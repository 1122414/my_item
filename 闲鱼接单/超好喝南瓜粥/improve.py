import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import random
from math import atan2, degrees, pi, cos
from collections import deque
from matplotlib.colors import LinearSegmentedColormap


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

    return obstacles

# A*算法实现
def a_star(graph, start, goal):
    return nx.astar_path(graph, start, goal)

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
    
    return probabilities

# 改进版基础距离算法
def base_distance_algorithm(current_node, goals, graph):
    """改进版基础距离算法"""
    # 计算到各目标的距离
    distances = [calculate_distance(graph, current_node, goal) for goal in goals]
    # 添加数值稳定性处理
    min_distance = min(distances)
    max_distance = max(distances)
    # 改进点1：使用指数衰减的权重计算
    # 添加可调节的温度参数（temperature）控制分布尖锐程度
    temperature = 0.5  # 值越小分布越尖锐
    # 改进点2：对距离进行标准化处理
    normalized_distances = [(d - min_distance + 1e-6) / (max_distance - min_distance + 1e-6) 
                          for d in distances]  # +1e-6防止除零
    # 改进点3：使用指数函数 + 非线性变换
    weights = [math.exp(-(d**1.5)/temperature) for d in normalized_distances]
    # 改进点4：添加拉普拉斯平滑
    alpha = 0.1  # 平滑系数
    total = sum(weights) + alpha * len(weights)
    # 生成概率分布
    probabilities = [(w + alpha)/total for w in weights]
    return probabilities

# 改进版步长花费算法（累积奖励+方向一致性）
def step_cost_algorithm(current_node, goals, graph, prev_node, history_steps=5, alpha=0.8):
    """改进版步长花费算法（累积奖励+方向一致性）"""
    if not prev_node:  # 初始状态
        return [1.0/len(goals)] * len(goals)
    
    # 初始化历史奖励记录（使用字典保存每个目标的奖励历史）
    if not hasattr(step_cost_algorithm, "reward_history"):
        step_cost_algorithm.reward_history = {goal: deque(maxlen=history_steps) for goal in goals}
    
    current_rewards = []
    directional_factors = []
    
    # 计算基础奖励和方向因子
    for i, goal in enumerate(goals):
        # 基础奖励计算
        prev_dist = calculate_distance(graph, prev_node, goal)
        curr_dist = calculate_distance(graph, current_node, goal)
        step_reward = prev_dist - curr_dist
        
        # 方向一致性计算（使用向量夹角）
        move_vector = np.array(current_node) - np.array(prev_node)
        target_vector = np.array(goal) - np.array(prev_node)
        
        # 计算夹角余弦值
        cos_sim = np.dot(move_vector, target_vector) / (
            np.linalg.norm(move_vector) * np.linalg.norm(target_vector) + 1e-6)
        directional_factor = max(cos_sim, 0)  # 仅考虑正向移动
        
        # 累积奖励计算（指数加权平均）
        history = step_cost_algorithm.reward_history[goal]
        if len(history) == 0:
            avg_reward = step_reward
        else:
            decay_factors = [alpha ** (history_steps - t) for t in range(len(history))]
            avg_reward = sum(r * f for r, f in zip(history, decay_factors)) / sum(decay_factors)
        
        # 综合奖励计算
        total_reward = step_reward + 0.5 * avg_reward + 0.3 * directional_factor * step_reward
        current_rewards.append(max(total_reward, 0))
        directional_factors.append(directional_factor)
        
        # 更新历史记录
        history.append(step_reward)
    
    # 动态温度参数（根据移动方向一致性调整）
    avg_direction = np.mean(directional_factors)
    temperature = 0.5 + 0.5 * (1 - avg_direction)  # 方向越分散，温度越高
    
    # 使用softmax归一化
    max_reward = max(current_rewards)
    exp_rewards = [math.exp((r - max_reward)/temperature) for r in current_rewards]
    total = sum(exp_rewards)
    
    if total == 0:
        return [1.0/len(goals)] * len(goals)
    
    return [er/total for er in exp_rewards]

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
                'step_cost': []
            },
            'last_processed_frame': -1
        }

    # 处理跳帧（填充缺失帧数据）
    current_frames = list(range(update.storage['last_processed_frame']+1, frame+1))
    for f in current_frames:
        update.storage['x_values'].append(f)
        for algo in ['my_algo', 'base_dist', 'step_cost']:
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
            # global last_position
            # last_position = current_position
            current_position = path[path_index] if path_index < len(path) else start
            current_goal = random.choice([g for g in goals if g in graph.nodes])
            path = a_star(graph, current_position, current_goal)
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

        # 计算三种算法的概率
        # my_prob = float(calculate_probability(current_node, goals, graph, {g:[] for g in goals})[0])
        # 只要目标点1的概率
        my_prob = float(calculate_probability(current_node, goals, graph, distance_record)[0])
        base_prob = float(base_distance_algorithm(current_node, goals, graph)[0])
        step_prob = float(step_cost_algorithm(current_node, goals, graph, prev_node)[0])
        prev_node = current_node

        # 更新当前帧的真实数据
        current_idx = len(update.storage['x_values']) - 1
        update.storage['prob_records']['my_algo'][current_idx] = my_prob
        update.storage['prob_records']['base_dist'][current_idx] = base_prob
        update.storage['prob_records']['step_cost'][current_idx] = step_prob

        # 绘制小球和轨迹
        global last_position_list
        global now_position 
        global last_position_num
        
        last_position_list[last_position_num%3] = now_position
        last_position_num += 1
        print(f"现在的last_position_list为：{last_position_list}")
        if last_position_num > 1 and (last_position_list[0]==last_position_list[1] or last_position_list[0]==last_position_list[2] or last_position_list[1]==last_position_list[2]):
            
            print("出现掉头情况")

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
        y_step = np.array(update.storage['prob_records']['step_cost'])[valid_indices]
        
        ax2.plot(x, y_my, color='blue', label='My Algorithm')
        ax2.plot(x, y_base, color='green', linestyle='--', label='Base Distance')
        ax2.plot(x, y_step, color='red', linestyle=':', label='Step Cost')
        
        # 动态显示最近30帧
        if len(x) > frame_num:
            ax2.set_xlim(x[-30], x[-1]+1)
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

    global last_position_list
    last_position_list = [0,0,0]

    # 控制last_position_list长度
    global last_position_num
    last_position_num = 0

    path = a_star(graph, start, current_goal)
    path_index = 0
    trajectory = []  # 用于存储小球的轨迹

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
