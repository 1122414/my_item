# 房间管理
# server/room_manager.py
import asyncio
import random
from common.protocol import MessageType
from common.constants import Suit, TILE_COUNTS

class Room:
    def __init__(self, room_id):
        self.room_id = room_id 
        self.players = []      # 玩家名称列表
        self.wall = []         # 牌墙
        self.discard_pile = [] # 弃牌堆
        self.current_player_index = 0  # 当前玩家索引
        self.status = 'waiting'        # 游戏状态
        self.game_over = False         # 新增游戏结束标志
        self.hands = {}                # 玩家手牌 {name: list}

    def initialize_wall(self):
        """生成136张麻将牌的正确实现"""
        tiles = []
        # 处理数牌（万/筒/条）
        for suit in [Suit.WAN, Suit.TONG, Suit.TIAO]:
            for num in range(1, 10):
                # 格式示例：1万, 2筒, 3条
                tiles += [f"{num}{suit.value}"] * 4
        
        # 处理字牌（东南西北中发白）
        honors = ['东','南','西','北','中','发','白']
        for h in honors:
            tiles += [h] * 4
        
        random.shuffle(tiles)
        self.wall = tiles
    
    def deal_initial_tiles(self):
        """初始发牌"""
        # 清空现有手牌
        self.hands = {name: [] for name in self.players}
        
        # 前三轮每人每次拿4张
        for _ in range(3):
            for player in self.players:
                self.hands[player].extend(self.wall[:4])
                self.wall = self.wall[4:]
        
        # 庄家多拿1张
        self.hands[self.players[0]].append(self.wall.pop(0))

class RoomManager:
    def __init__(self, server):
        self.rooms = {}         # {room_id: Room实例}
        self.room_counter = 0
        self.player_room_map = {}  # 新增玩家映射字典 {player_name: room_id}
        self.server = server  # 新增服务器引用

    # def create_room(self):
    #     self.room_counter += 1
    #     room = Room(f"room_{self.room_counter}")
    #     room.initialize_wall()
    #     self.rooms[room.room_id] = room
    #     return room

    async def assign_room(self, player_name):
        """异步分配房间"""
        # 查找已有房间
        for room in self.rooms.values():
            if len(room.players) < 4:
                room.players.append(player_name)
                self.player_room_map[player_name] = room.room_id
                
                # 新增满员检查
                if len(room.players) == 4:
                    await self.start_game(room)
                return room
        
        # 创建新房间
        self.room_counter += 1
        new_room = Room(f"room_{self.room_counter}")
        new_room.players.append(player_name)
        self.rooms[new_room.room_id] = new_room
        self.player_room_map[player_name] = new_room.room_id
        return new_room
    
    async def check_room_ready(self, room):
        """增强的房间就绪检查"""
        if len(room.players) == 4:
            # 检查所有玩家是否完成连接握手
            all_ready = all(
                player in self.server.connections
                for player in room.players
            )
            if all_ready:
                print(f"房间 {room.room_id} 准备就绪，开始游戏")
                await self.server.start_game(room)
            else:
                print(f"房间 {room.room_id} 有玩家未完成连接")

    async def start_game(self, room):
        """异步启动游戏"""
        print(f"房间 {room.room_id} 开始游戏流程")
        
        # 初始化游戏状态
        room.initialize_wall()
        room.deal_initial_tiles()
        room.status = 'playing'
        
        # 创建游戏循环任务
        asyncio.create_task(
            self.server._game_loop(room),
            name=f"game_loop_{room.room_id}"
        )
        
        # 通知所有玩家
        await self.server._broadcast(
            room,
            MessageType.GAME_START,
            {
                "players": room.players,
                "wall_count": len(room.wall)
            }
        )