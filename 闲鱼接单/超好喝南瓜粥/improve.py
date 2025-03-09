import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import random
import threading
from math import atan2, degrees, pi, cos
from collections import deque
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime


current_path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(current_path, 'data.txt')
graph_file_path = os.path.join(current_path, 'graph.png')

# 计算夹角
def cal_included_angle():
    """
    计算上一步与目标连线  然后这一步跟上一步连线  这两根线的夹角（单位：度）
    返回：0.0-180.0之间的角度值，轨迹不足三点时返回0.0
    """
    global trajectory
    
    if len(trajectory) < 3:
        return 0.0
    
    # 获取最近三个轨迹点
    a, b = trajectory[-2], trajectory[-1]
    
    # 坐标转换（复用已有的hex_to_cartesian逻辑）
    def hex_to_cartesian(node):
        q, r, _ = node
        x = q * np.sqrt(3) + r * np.sqrt(3)/2
        y = r * 1.5
        return np.array([x, y])
    
    # 转换为笛卡尔坐标
    a_pt = hex_to_cartesian(a)
    b_pt = hex_to_cartesian(b)
    c_pt = hex_to_cartesian(goals[0])
    
    # 计算向量 AC 和 AB
    vector_ba = c_pt - a_pt  # 前一个方向向量
    vector_bc = b_pt - a_pt  # 当前方向向量
    
    # 计算夹角（使用向量点积公式）
    dot_product = np.dot(vector_ba, vector_bc)
    norm_ba = np.linalg.norm(vector_ba)
    norm_bc = np.linalg.norm(vector_bc)
    
    if norm_ba == 0 or norm_bc == 0:
        return 0.0
    
    cos_theta = dot_product / (norm_ba * norm_bc)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)  # 处理浮点误差
    angle = np.degrees(np.arccos(cos_theta))
    
    return round(angle, 2)  # 保留两位小数

# 生成六边形棋盘
def generate_hexagonal_grid(size):
    grid = []
    for q in range(-size, size + 1):
        for r in range(max(-size, -q - size), min(size, -q + size) + 1):
            grid.append((q, r, -q - r))
    return grid

# 定义障碍物
def generate_obstacles(grid, num_obstacles, obstacle_size):
    obstacles = []
    forbidden_nodes = {start, *goals}   # 定义关键点集合（起点 + 所有目标点）
    candidate_nodes = [node for node in grid if node not in forbidden_nodes]     # 排除关键点
    for _ in range(num_obstacles):
        # 随机选择一个非关键点作为障碍物中心
        center = candidate_nodes[np.random.randint(0, len(candidate_nodes))]
        obstacle = []
        # 生成障碍物区域
        for q in range(center[0] - obstacle_size, center[0] + obstacle_size + 1):
            for r in range(center[1] - obstacle_size, center[1] + obstacle_size + 1):
                node = (q, r, -q - r)
                # 检查节点是否在网格内，且不在关键点上
                if node in grid and node not in forbidden_nodes:
                    obstacle.append(node)
        obstacles.append(obstacle)
        # 更新候选节点，排除已生成的障碍物区域
        candidate_nodes = [node for node in candidate_nodes if node not in obstacle]
    # print(f"目前的obstacles是:{obstacles}")
    return obstacles

# 给a*添加扰动
def weighted_heuristic(u, v):
    # 原始启发式（如曼哈顿距离）
    base = abs(u[0] - v[0]) + abs(u[1] - v[1])
    # 增加随机扰动（权重范围可调）
    return base * (0.9 + random.uniform(0, 0.3))  # 随机扰动10%~20%
# A*算法实现
def a_star(graph, start, goal):
    return nx.astar_path(graph, start, goal, heuristic=weighted_heuristic)

# 绘制六边形
def draw_hexagon(ax, q, r, color='white'):
    # x,y坐标
    x = q * np.sqrt(3) + r * np.sqrt(3) / 2
    y = r * 1.5
    hexagon = plt.Polygon([
        (x + np.sqrt(3) / 2, y + 0.5),
        (x, y + 1),
        (x - np.sqrt(3) / 2, y + 0.5),
        (x - np.sqrt(3) / 2, y - 0.5),
        (x, y - 1),
        (x + np.sqrt(3) / 2, y - 0.5)
    ], closed=True, edgecolor='black', facecolor=color)
    ax.add_patch(hexagon)
    return x,y

# 计算距离（最少格子数）
def calculate_distance(graph, start, goal):
    try:
        path = a_star(graph, start, goal)
        return len(path) - 1  # 距离为路径长度减1
    except nx.NetworkXNoPath:
        return float('inf')  # 如果无法到达目标点，返回无穷大

# 计算概率
def calculate_probability(current_node, goals, graph, distance_record):
    # 步长，即过去n步的记录
    n = 3

    # 更改部分
    # 计算到各目标的距离
    distances = [calculate_distance(graph, current_node, goal) for goal in goals]
    # 记录距离数据
    for i, goal in enumerate(goals):
        distance_record[goal].append(distances[i])
    # 检查是否到达任意目标点
    for i, d in enumerate(distances):
        if d == 0:
            # 生成概率向量（1对应到达的目标，其余为0）
            prob = [0.0] * len(goals)
            prob[i] = 1.0
            return tuple(prob)
    # 初始化所有theta为默认值
    thetas = [np.pi/2] * len(goals)
    # 初始化
    d_map_pi = 1.0  
    # 当有足够历史数据时计算趋势
    if len(distance_record[goals[0]]) >= n:
        x = list(range(1,n+1))  # 时间序列
        for i in range(len(goals)):
            # 获取最近5个距离值
            y = distance_record[goals[i]][-n:]
            # 步长映射
            d_change = y[0]-y[n-1]
            d_map_pi = math.pi*(d_change+n)/n

            # 计算线性回归系数
            coef = np.polyfit(x, y, 1)[0]
            # 计算角度（趋势方向）
            thetas[i] = np.arctan(coef)
    # 计算各目标权重
    weights = []
    for i in range(len(goals)):
        x = distances[i]
        theta = thetas[i]
        # 权重计算公式（可根据需要调整系数）
        weight = d_map_pi * (1 / (x**2 + 1)) * (0.6 * np.cos(theta)**2 + 1.4 * np.cos(theta) + 1)
        weights.append(weight)
    # 归一化处理
    total = sum(weights)
    probabilities = [w/total for w in weights]
    global not_nan_pro
    if not math.isnan(probabilities[0]):
        not_nan_pro = probabilities[0]

    if math.isnan(probabilities[0]):
        print(f"pre_probabilities[0]:{probabilities[0]}")
        probabilities[0] = not_nan_pro
        print(f"d_map_pi{d_map_pi},w{weights[0]},total{total}")
        print(f"probabilities[0]:{probabilities[0]}")

    return probabilities

# 改进版基础距离算法
def base_distance_algorithm(current_node, goals, graph):
    """最基础的距离算法"""
    # 计算到各目标点的距离
    distances = []
    for goal in goals:
        try:
            # 使用networkx的最短路径算法
            distances.append(nx.shortest_path_length(graph, current_node, goal))
        except nx.NetworkXNoPath:
            distances.append(float('inf'))

    # 处理所有目标都不可达的情况
    if all(d == float('inf') for d in distances):
        return [1.0/len(goals)] * len(goals)
    
    # 计算基础权重（距离的倒数）
    weights = []
    for d in distances:
        if d == float('inf'):
            weights.append(0)
        else:
            # 加1防止除零，当d=0时（已到达目标）权重为1
            weights.append(1/(d**2 + 1))  

    # 处理起点特殊情况：当所有可达目标的距离相等时均分概率
    valid_distances = [d for d in distances if d != float('inf')]
    if len(set(valid_distances)) == 1 and valid_distances[0] == nx.shortest_path_length(graph, start, start):
        return [1.0/len(valid_distances) if d != float('inf') else 0 for d in distances]

    # 归一化处理
    total = sum(weights)
    if total == 0:
        return [1.0/len(goals)] * len(goals)
    
    return [w/total for w in weights]

# 角度算法
def angle_algorithm(current_node, goals, graph, prev_node):
    """平滑版方向概率算法"""
    # 初始化历史记录
    if not hasattr(angle_algorithm, "history"):
        angle_algorithm.history = {
            'move_vectors': deque(maxlen=3),  # 保存最近3个移动方向
            'prev_weights': None
        }
    
    # 初始状态处理
    if not prev_node:
        return [1.0/len(goals)] * len(goals)
    
    # 坐标转换
    def hex_to_cartesian(node):
        q, r, _ = node
        x = q * np.sqrt(3) + r * np.sqrt(3)/2
        y = r * 1.5
        return np.array([x, y])
    
    # 获取当前移动向量
    current_pos = hex_to_cartesian(current_node)
    prev_pos = hex_to_cartesian(prev_node)
    move_vector = current_pos - prev_pos
    move_norm = np.linalg.norm(move_vector)
    
    # 平滑处理：使用3帧指数衰减平均
    angle_algorithm.history['move_vectors'].append(move_vector)
    weights = [0.5**i for i in range(len(angle_algorithm.history['move_vectors']))]
    weights = np.array(weights[::-1])/sum(weights)  # 最近帧权重最大
    smoothed_move = sum(vec*w for vec,w in zip(angle_algorithm.history['move_vectors'], weights))
    
    # 计算各目标权重
    weights = []
    for goal in goals:
        goal_pos = hex_to_cartesian(goal)
        target_vector = goal_pos - current_pos
        target_norm = np.linalg.norm(target_vector)
        
        # 到达目标直接返回
        if target_norm < 1e-6:
            return [1.0 if g == goal else 0.0 for g in goals]
        
        # 计算平滑后的方向一致性
        cos_sim = np.dot(smoothed_move, target_vector) / (np.linalg.norm(smoothed_move)*target_norm + 1e-6)
        directional_weight = (cos_sim + 1) / 2  # 策略2
        
        # 添加距离衰减因子
        distance = calculate_distance(graph, current_node, goal)
        distance_weight = 1/(distance + 1)
        
        # 综合权重（可调比例）
        total_weight = 0.7*directional_weight + 0.3*distance_weight
        weights.append(total_weight)
    
    # 添加历史惯性（防止突变）
    if angle_algorithm.history['prev_weights'] is not None:
        weights = [0.3*old + 0.7*new for old,new in zip(angle_algorithm.history['prev_weights'], weights)]
    angle_algorithm.history['prev_weights'] = weights
    
    # 归一化处理
    total = max(sum(weights), 1e-10)
    return [w/total for w in weights]

# 广度优先搜索计算最短距离
def bfs_shortest_distance(graph, start):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    queue = deque([start])

    while queue:
        current_node = queue.popleft()
        for neighbor in graph.neighbors(current_node):
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[current_node] + 1
                queue.append(neighbor)
    return distances

# 动画更新函数
def update(frame):
    # 初始化持久化存储结构
    if not hasattr(update, "storage"):
        update.storage = {
            'x_values': [],
            'prob_records': {
                'my_algo': [],
                'base_dist': [],
                'angle': []
            },
            'last_processed_frame': -1
        }

    # 处理跳帧（填充缺失帧数据）
    current_frames = list(range(update.storage['last_processed_frame']+1, frame+1))
    for f in current_frames:
        update.storage['x_values'].append(f)
        for algo in ['my_algo', 'base_dist', 'angle']:
            if len(update.storage['prob_records'][algo]) == 0:
                update.storage['prob_records'][algo].append(None)
            else:
                update.storage['prob_records'][algo].append(
                    update.storage['prob_records'][algo][-1]
                )
    
    # 更新最后处理的帧号
    update.storage['last_processed_frame'] = frame

    # 全局变量声明
    global path_index, current_goal, path, trajectory, prev_node, distance_record
    
    # 清空画布
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # 隐藏坐标轴
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_aspect('equal')
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_aspect('equal')

    # 绘制六边形网格
    for node in grid:
        color = 'white'
        if node in [item for sublist in obstacles for item in sublist]:
            color = 'gray'
        if node == start:
            color = 'blue'
        if node in goals:
            idx = goals.index(node)
            color = ['yellow', 'green', 'red', 'purple', 'orange'][idx]
        draw_hexagon(ax1, node[0], node[1], color)
        draw_hexagon(ax3, node[0], node[1], color)

    # 每隔10秒重新选择目标点
    if frame % 10 == 0 and frame != 0:
        try:
            # global current_position
            global last_position
            # last_position = current_position
            current_position = path[path_index] if path_index < len(path) else start
            current_goal = random.choice([g for g in goals if g in graph.nodes])
            # print(f"current_position:{current_position},current_goal:{current_goal}")
            # print(f"last_path:{path}")
            last_position = path[path_index-1]
            # print(f"last_position:{last_position}")
            path = a_star(graph, current_position, current_goal)
            # print(f"change_path:{path}")
            try_num=0
            while last_position == path[1]:
                # a*回头 重新生成a*路径
                try_num+=1
                print(f"last_path:{path}")
                path = a_star(graph, current_position, current_goal)
                print(f"change_path:{path}")
                if try_num>10:
                    print("a*必回头")
                    break

                print("出现掉头情况，请及时修改")

            # 处理掉头
            # if last_position == path[1]:
            #     path[1][0]+2
            #     print("掉头情况")
            path_index = 0
            # 如果目标点数大于 goal_num 则清空轨迹
            # if len(goals)>=goal_num:
            #     trajectory.clear()  # 仅清除轨迹，不重置概率数据
        except Exception as e:
            print(f"重新选择目标点时出现错误：{e}")
            path = [start]
            path_index = 0

    # 更新小球位置
    if path_index < len(path) and path_index >= 0:
        current_node = path[path_index]
        trajectory.append(current_node)
        # 检查是否到达目标点
        if current_node in goals:
            trajectory.clear()  # 清空当前轨迹
            ax1.clear()
            ax3.clear()
            print(f"已到达目标点 {current_node}，轨迹已清空")

        # 计算三种算法的概率
        # my_prob = float(calculate_probability(current_node, goals, graph, {g:[] for g in goals})[0])
        # 只要目标点1的概率
        my_prob = float(calculate_probability(current_node, goals, graph, distance_record)[0])
        base_prob = float(base_distance_algorithm(current_node, goals, graph)[0])
        step_prob = float(angle_algorithm(current_node, goals, graph, prev_node)[0])
        prev_node = current_node
        
        # 打印夹角
        now_angle = cal_included_angle()
        print(f"now_angle:{now_angle}")

        # 更新当前帧的真实数据
        current_idx = len(update.storage['x_values']) - 1
        update.storage['prob_records']['my_algo'][current_idx] = my_prob
        update.storage['prob_records']['base_dist'][current_idx] = base_prob
        update.storage['prob_records']['angle'][current_idx] = step_prob

        # 绘制小球和轨迹
        global last_position_list
        global now_position 
        global last_position_num

        now_position = draw_hexagon(ax1, current_node[0], current_node[1], 'green')

        # print(f"过去的节点是：{last_position_list},现在的节点是：{now_position}")
        draw_hexagon(ax3, current_node[0], current_node[1], 'red')
        if len(trajectory) > 1:
            x_coords = [n[0]*np.sqrt(3)+n[1]*np.sqrt(3)/2 for n in trajectory]
            y_coords = [n[1]*1.5 for n in trajectory]
            ax1.plot(x_coords, y_coords, color='orange', linewidth=2)
            ax3.plot(x_coords, y_coords, color='orange', linewidth=2)
        
        path_index += 1

    # 绘制概率曲线
    valid_indices = [i for i, v in enumerate(update.storage['prob_records']['my_algo']) if v is not None]
    if valid_indices:
        x = np.array(update.storage['x_values'])[valid_indices]
        y_my = np.array(update.storage['prob_records']['my_algo'])[valid_indices]
        y_base = np.array(update.storage['prob_records']['base_dist'])[valid_indices]
        y_step = np.array(update.storage['prob_records']['angle'])[valid_indices]
        # print(f"y_my:{y_my}")
        ax2.plot(x, y_my, color='blue', label='My Algorithm')
        ax2.plot(x, y_base, color='green', linestyle='--', label='Base Distance')
        ax2.plot(x, y_step, color='red', linestyle=':', label='Step Cost')
        
        # 动态显示最近30帧
        if len(x) > frame_num:
            ax2.set_xlim(x[-frame_num], x[-1]+1)
        else:
            ax2.set_xlim(x[0]-1, x[-1]+1)
    else:
        ax2.text(0.5, 0.5, 'Waiting for data...', ha='center', va='center')
    
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Frame')
    ax2.set_ylabel('Probability')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_title("Goal 1 Probability Comparison")

    # 绘制最短距离图
    max_distance = max(amin_distances.values())
    for node in grid:
        if node not in [item for sublist in obstacles for item in sublist] and node not in goals:
            x = node[0] * np.sqrt(3) + node[1] * np.sqrt(3)/2
            y = node[1] * 1.5
            distance = amin_distances[node]
            color = cmap(distance / max_distance)
            draw_hexagon(ax3, node[0], node[1], color)
            ax3.text(x, y, f"{distance}", ha='center', va='center', fontsize=3)

    plt.title(f"Frame: {frame}")
    return ax1, ax2, ax3



if __name__ == "__main__":
    global save_counter
    save_counter = 0  # 保存次数计数器
    
    # 将地图变大、目标变多 更改
    # 初始化棋盘
    size = 18

    # 定义起点和目标点
    start = (-size, 0, size)

    # 将地图变大、目标变多
    # goals = [(size, -size, 0), (0, size, -size),  (0, -size, size), (size, 0, -size), (-size, size, 0), ]  # 五个目标点 更改
    goals = [(size, -size, 0), (0, size, -size),   ]  # 五个目标点 更改

    grid = generate_hexagonal_grid(size)
    obstacles = generate_obstacles(grid, 4, 2)

    # 创建图并添加边
    graph = nx.Graph()
    for node in grid:
        if node not in [item for sublist in obstacles for item in sublist]:
            for neighbor in [(node[0] + 1, node[1], node[2] - 1),
                             (node[0] - 1, node[1], node[2] + 1),
                             (node[0], node[1] + 1, node[2] - 1),
                             (node[0], node[1] - 1, node[2] + 1),
                             (node[0] + 1, node[1] - 1, node[2]),
                             (node[0] - 1, node[1] + 1, node[2])]:
                if neighbor in grid and neighbor not in [item for sublist in obstacles for item in sublist]:
                    graph.add_edge(node, neighbor)

    # 初始化路径
    current_goal = random.choice(goals)  # 随机选择一个目标点
    global distance_record 
    distance_record = {goal: [] for goal in goals}  # 用于记录每个目标点到起点的距离

    # 当目标点数大于goal_num时，则清空小球轨迹
    global goal_num 
    goal_num = 4

    # 动态显示最近frame_num帧
    global frame_num
    frame_num = 30

    # 当前位置，设为全局处理掉头
    global now_position
    now_position = (0,0)

    global last_position
    last_position = (0,0,0)

    global last_position_list
    last_position_list = [0,0,0]

    # 控制last_position_list长度
    global last_position_num
    last_position_num = 0

    global trajectory

    path = a_star(graph, start, current_goal)
    path_index = 0
    trajectory = []  # 用于存储小球的轨迹

    global not_nan_pro
    not_nan_pro = 0

    recorded_frames = set()  # 用于跟踪已记录帧
    prev_node = None  # 添加历史节点追踪

    probabilities = [[] for _ in goals]  # 每个目标一个概率列表
    # probabilities = []  # 用于存储概率
    yplus_values = []  # 用于存储 yplus 的值
    time_points = []  # 用于存储时间点

    # 计算每个网格到目标点1的最短距离
    amin_distances = bfs_shortest_distance(graph, goals[0])

    # 定义颜色映射（浅橘色到浅黄色）
    colors = ["#FFE5B4", "#FFD700"]  # 浅橘色到浅黄色
    cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)
    # 创建动画
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 8))
    # ani = animation.FuncAnimation(fig, update, frames=100, interval=100, blit=False)  # 100帧，每秒1帧
    ani = animation.FuncAnimation(
    fig, 
    update, 
    frames=None,  # 使用生成器无限生成帧
    interval=100,
    blit=False,
    repeat=False,  # 禁用循环
    save_count=1000  # 适当调大缓存
    )
    plt.show()

    # 获取存储的数据
    x_values = update.storage['x_values']
    my_probs = update.storage['prob_records']['my_algo']
    base_probs = update.storage['prob_records']['base_dist']
    angle_probs = update.storage['prob_records']['angle']

    # 创建DataFrame并清理数据
    df = pd.DataFrame({
        'Frame': x_values,
        'My_Algorithm': my_probs,
        'Base_Distance': base_probs,
        'Angle_Algorithm': angle_probs
    }).dropna()

    # 保存CSV数据
    df.to_csv('probability_data.csv', index=False)
    print("概率数据已保存到 probability_data.csv")

    # 绘制最终折线图
    plt.figure(figsize=(12, 6))
    plt.plot(df['Frame'], df['My_Algorithm'], 'b-', label='My Algorithm')
    plt.plot(df['Frame'], df['Base_Distance'], 'g--', label='Base Distance')
    plt.plot(df['Frame'], df['Angle_Algorithm'], 'r:', label='Angle Algorithm')
    
    plt.xlabel('Frame Number')
    plt.ylabel('Probability')
    plt.title('Goal 1 Probability Comparison Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # 保存图片
    plt.savefig('final_probability_plot.png', dpi=300)
    print("折线图已保存为 final_probability_plot.png")
    plt.close()
