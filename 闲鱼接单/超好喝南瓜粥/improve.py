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


# 计算距离（最少格子数）
def calculate_distance(graph, start, goal):
    try:
        path = a_star(graph, start, goal)
        return len(path) - 1  # 距离为路径长度减1
    except nx.NetworkXNoPath:
        return float('inf')  # 如果无法到达目标点，返回无穷大


# 计算概率
def calculate_probability(current_node, goals, graph, distance_record):
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
    # 当有足够历史数据时计算趋势
    if len(distance_record[goals[0]]) >= 5:
        x = [1, 2, 3, 4, 5]  # 时间序列
        for i in range(len(goals)):
            # 获取最近5个距离值
            y = distance_record[goals[i]][-5:]
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
        weight = (1 / (x**2 + 1)) * (0.6 * np.cos(theta)**2 + 1.4 * np.cos(theta) + 1)
        weights.append(weight)
    # 归一化处理
    total = sum(weights)
    probabilities = [w/total for w in weights]
    
    return tuple(probabilities)

    # region
    # x1 = calculate_distance(graph, current_node, goals[0])  # 到目标点1的距离
    # x2 = calculate_distance(graph, current_node, goals[1])  # 到目标点2的距离
    # x3 = calculate_distance(graph, current_node, goals[2])  # 到目标点3的距离
    # x4 = calculate_distance(graph, current_node, goals[3])  # 到目标点4的距离
    # x5 = calculate_distance(graph, current_node, goals[4])  # 到目标点5的距离

    # distance_record[goals[0]].append(x1)  # 记录每次计算的最短距离
    # distance_record[goals[1]].append(x2)
    # distance_record[goals[2]].append(x3)
    # distance_record[goals[3]].append(x4)
    # distance_record[goals[4]].append(x5)

    # # 如果小球到达目标点1
    # if x1 == 0:
    #     return 1.0, 0.0, 0.0, 0.0, 0.0  # 概率为1和0
    # # 如果小球到达目标点2
    # if x2 == 0:
    #     return 0.0, 1.0, 0.0, 0.0, 0.0  # 概率为0和1
    # # 如果小球到达目标点3
    # if x3 == 0:
    #     return 0.0, 0.0, 1.0, 0.0, 0.0  # 概率为0和1
    # # 如果小球到达目标点4
    # if x4 == 0:
    #     return 0.0, 0.0, 0.0, 1.0, 0.0  # 概率为0和1
    # # 如果小球到达目标点5
    # if x5 == 0:
    #     return 0.0, 0.0, 0.0, 0.0, 1.0  # 概率为0和1


    # # 计算概率
    # if len(distance_record[goals[0]]) >= 5:  # 依据过5步，通过一元线性回归做方向判断
    #     x = [1, 2, 3, 4, 5]
    #     y1 = distance_record[goals[0]][len(distance_record[goals[0]]) - 5: len(distance_record[goals[0]]) - 1]
    #     y2 = distance_record[goals[1]][len(distance_record[goals[1]]) - 5: len(distance_record[goals[1]]) - 1]
    #     y3 = distance_record[goals[3]][len(distance_record[goals[3]]) - 5: len(distance_record[goals[3]]) - 1]
    #     y4 = distance_record[goals[4]][len(distance_record[goals[4]]) - 5: len(distance_record[goals[4]]) - 1]
    #     y5 = distance_record[goals[5]][len(distance_record[goals[5]]) - 5: len(distance_record[goals[5]]) - 1]

    #     coef1 = np.polyfit(x, y1, 1)[0]
    #     coef2 = np.polyfit(x, y2, 1)[0]
    #     coef3 = np.polyfit(x, y3, 1)[0]
    #     coef4 = np.polyfit(x, y4, 1)[0]
    #     coef5 = np.polyfit(x, y5, 1)[0]

    #     theta1 = np.arctan(coef1)
    #     theta2 = np.arctan(coef2)
    #     theta3 = np.arctan(coef3)
    #     theta4 = np.arctan(coef4)
    #     theta5 = np.arctan(coef5)

    # else:
    #     theta1 = theta2 = np.pi / 2
    # m = 1 / (x1 ** 2 + 1) * (0.6 * cos(theta1) ** 2 + 1.4 * cos(theta1) + 1)
    # n = 1 / (x2 ** 2 + 1) * (0.6 * cos(theta2) ** 2 + 1.4 * cos(theta2) + 1)
    # total = m + n
    # m /= total
    # n /= total
    # return m, n
    #endregion

# 在calculate_probability函数后添加两个新算法

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

# 2025.3.6 与我的算法重合
# def base_distance_algorithm(current_node, goals, graph):
#     """基础距离算法"""
#     distances = [calculate_distance(graph, current_node, goal) for goal in goals]
#     weight = [1/(d**2 + 1) for d in distances]
#     total = sum(weight)
#     return [w/total for w in weight]
#     # # 计算指数值（带数值稳定性处理）
#     # max_V = max(-d for d in distances)
#     # exp_values = [math.exp(-d - max_V) for d in distances]  # 防止数值溢出
#     # # 计算总和
#     # total = sum(exp_values)
#     # 归一化处理
#     # return [ev/total for ev in exp_values]

# 2025.3.6改进版
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

# def step_cost_algorithm(current_node, goals, graph, prev_node):
#     """步长花费算法"""
#     if not prev_node:  # 初始状态没有前一个节点
#         return [1.0/len(goals)]*len(goals)
    
#     costs = []
#     for i, goal in enumerate(goals):
#         # 原始最短距离
#         orig_dist = calculate_distance(graph, prev_node, goal)
#         # 移动后距离
#         new_dist = calculate_distance(graph, current_node, goal)
#         cost = orig_dist - new_dist
#         costs.append(max(cost, 0))  # 负成本视为0
    
#     total = sum(math.e**c for c in costs)
#     if total == 0:
#         return [1.0/len(goals)]*len(goals)  # 平均概率
#     return [math.e**c/total for c in costs]

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
    # 在update函数开头添加样式设置
    # plt.style.use('seaborn')  # 使用更清晰的绘图样式
    colors = ['yellow', 'green', 'red', 'purple', 'orange']
    global path_index, current_goal, path, trajectory, prob_records, probabilities, yplus_values, time_points, prev_node, recorded_frames
    # 初始化时确保数据结构有效
    if not time_points:
        time_points[:] = []
        prob_records['my_algo'][:] = []
        prob_records['base_dist'][:] = []
        prob_records['step_cost'][:] = []
    
    # 在绘制前检查数据同步
    min_len = min(len(time_points), 
                 len(prob_records['my_algo']),
                 len(prob_records['base_dist']),
                 len(prob_records['step_cost']))
    
    # 同步裁剪数据
    time_points = time_points[:min_len]
    prob_records['my_algo'] = prob_records['my_algo'][:min_len]
    prob_records['base_dist'] = prob_records['base_dist'][:min_len]
    prob_records['step_cost'] = prob_records['step_cost'][:min_len]
    
    ax1.clear()  # 清空棋盘
    ax2.clear()  # 清空概率图
    ax3.clear()  # 清空最短距离图

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
            color = 'gray'  # 障碍物
        if node == start:
            color = 'blue'  # 起点
        if node in goals:
            idx = goals.index(node)
            color = colors[idx]  # 目标点
        draw_hexagon(ax1, node[0], node[1], color)
        draw_hexagon(ax3, node[0], node[1], color)

    # 每隔10秒重新选择目标点
    if frame % 10 == 0 and frame != 0:
        try:
            # 确保使用有效路径节点
            current_position = path[path_index] if path_index < len(path) else start
            current_goal = random.choice([g for g in goals if g in graph.nodes])
            path = a_star(graph, current_position, current_goal)
            path_index = 0  # 重置后从0开始
        except Exception as e:
            print(f"路径重置失败: {str(e)}")
            path = [start]  # 重置路径
            path_index = 0
        # 清空数据时保持引用
        del prob_records['my_algo'][:]
        del prob_records['base_dist'][:]
        del prob_records['step_cost'][:]
        time_points.clear()
        recorded_frames.clear()
        # prob_records['my_algo'].clear()
        # prob_records['base_dist'].clear()
        # prob_records['step_cost'].clear()
        # time_points.clear()
        # recorded_frames.clear()

    # 计算概率
    distance_record = {goal: [] for goal in goals}  # 为每个目标创建记录列表
    # 绘制小球的轨迹
    if path_index < len(path) and path_index >= 0:
        current_node = path[path_index]
        # 强制同步记录（每个移动步骤都记录）
        my_prob = float(calculate_probability(current_node, goals, graph, distance_record)[0])
        base_prob = float(base_distance_algorithm(current_node, goals, graph)[0])
        step_prob = float(step_cost_algorithm(current_node, goals, graph, prev_node)[0])
        
        prob_records['my_algo'].append(my_prob)
        prob_records['base_dist'].append(base_prob)
        prob_records['step_cost'].append(step_prob)
        time_points.append(frame)
        recorded_frames.add(frame)

        trajectory.append(current_node)  # 记录轨迹
        draw_hexagon(ax1, current_node[0], current_node[1], 'red')
        draw_hexagon(ax3, current_node[0], current_node[1], 'red')  # 小球
        path_index += 1

    # 绘制小球的轨迹线
    if len(trajectory) > 1:
        x_coords = [node[0] * np.sqrt(3) + node[1] * np.sqrt(3) / 2 for node in trajectory]
        y_coords = [node[1] * 1.5 for node in trajectory]
        ax1.plot(x_coords, y_coords, color='orange', linewidth=2)
        ax3.plot(x_coords, y_coords, color='orange', linewidth=2)

    if path_index < len(path) and path_index > 0:
        current_node = path[path_index]

        # 计算概率
        probs = calculate_probability(current_node, goals, graph, distance_record)

        # 记录数据
        for i in range(len(goals)):
            probabilities[i].append(probs[i])
        time_points.append(frame)
        
    # 计算三种算法的概率
    current_node = path[path_index] if path_index < len(path) else start
    
    # 原算法
    my_probs = calculate_probability(current_node, goals, graph, distance_record)
    
    # 基础距离算法
    base_probs = base_distance_algorithm(current_node, goals, graph)
    
    # 步长花费算法
    step_probs = step_cost_algorithm(current_node, goals, graph, prev_node)
    prev_node = current_node  # 更新前节点

    # 记录目标1的概率
    # for algo, probs in zip(['my_algo', 'base_dist', 'step_cost'], 
    #                       [my_probs, base_probs, step_probs]):
    #     prob_records[algo][0].append(probs[0])  # 只记录目标1
    for algo, prob in zip(['my_algo', 'base_dist', 'step_cost'], 
                     [my_probs[0], base_probs[0], step_probs[0]]):
        prob_records[algo].append(prob)  # 直接记录目标1的概率值


    # 绘制概率的折线图
    # colors = ['yellow', 'green', 'red', 'purple', 'orange']
    # for i in range(len(goals)):
    #     ax2.plot(time_points, probabilities[i], 
    #             color=colors[i], 
    #             label=f'Goal {i+1} Probability')
        
    # # 绘制曲线时直接使用当前记录
    # ax2.plot(np.array(time_points), np.array(prob_records['my_algo']), color='blue', label='My Algorithm')
    # ax2.plot(np.array(time_points), np.array(prob_records['base_dist']), color='green', linestyle='--', label='Base Distance')
    # ax2.plot(np.array(time_points), np.array(prob_records['step_cost']), color='red', linestyle=':', label='Step Cost')
    # 在绘图前添加强制同步
    min_len = min(len(time_points), 
                len(prob_records['my_algo']),
                len(prob_records['base_dist']),
                len(prob_records['step_cost']))

    # 生成安全索引
    x = np.arange(min_len)
    if min_len > 0:
        ax2.plot(x, prob_records['my_algo'][:min_len], color='blue', label='My Algorithm')
        ax2.plot(x, prob_records['base_dist'][:min_len], color='green', linestyle='--', label='Base Distance')
        ax2.plot(x, prob_records['step_cost'][:min_len], color='red', linestyle=':', label='Step Cost')
    else:
        ax2.text(0.5, 0.5, 'No Data', ha='center', va='center')  # 空数据提示

    # ax2.plot(time_points, probabilities, color='blue', label='Mine Algorithm Probability to Goal 1')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Value')
    ax2.set_ylim(0, 1)
    # 修改图例位置和样式
    ax2.legend(loc='upper right', frameon=True, shadow=True)
    # 添加网格线
    ax2.grid(True, alpha=0.3)
    # 设置标题
    ax2.set_title("Goal 1 Probability Comparison", fontsize=12)

    # 绘制最短距离图
    max_distance = max(amin_distances.values())  # 最大距离
    for node in grid:
        if node not in [item for sublist in obstacles for item in sublist] and node not in goals:
            x = node[0] * np.sqrt(3) + node[1] * np.sqrt(3) / 2
            y = node[1] * 1.5
            distance = amin_distances[node]
            color = cmap(distance / max_distance)  # 根据距离设置颜色
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
    goals = [(size, -size, 0), (0, size, -size),  (0, -size, size), (size, 0, -size), (-size, size, 0), ]  # 五个目标点 更改

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
    path = a_star(graph, start, current_goal)
    path_index = 0
    trajectory = []  # 用于存储小球的轨迹

    recorded_frames = set()  # 用于跟踪已记录帧
    # 修改prob_records初始化结构
    prob_records = {
        'my_algo': list(),
        'base_dist': list(),
        'step_cost': list()
    }
    time_points = list()
    recorded_frames = set()

    # 概率初始化
    # prob_records = {
    #     'my_algo': [[] for _ in goals],   # 原算法
    #     'base_dist': [[] for _ in goals], # 基础距离算法
    #     'step_cost': [[] for _ in goals]  # 步长花费算法
    # }
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
    ani = animation.FuncAnimation(fig, update, frames=100, interval=100, blit=False)  # 100帧，每秒1帧
    plt.show()
