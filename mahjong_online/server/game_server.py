# 主服务程序# server/game_server.py 完整代码
import time
import asyncio
import websockets
from collections import defaultdict
from .room_manager import RoomManager
from common.protocol import GameProtocol, MessageType

class MahjongServer:
    def __init__(self):
        #1. self.connected_players = set()
        # 修改后：传递self作为server参数
        self.room_manager = RoomManager(self)  
        self.connections = {}
        self.message_queues = defaultdict(asyncio.Queue)  # 新增消息队列
        self.heartbeat_allowed = {}  # 新增心跳许可状态
        self.websocket_to_player = {}  # 新增映射关系

    #1. async def handle_client(self, websocket):
    #   try:
    #       self.connected_players.add(websocket)
    #       print(f"新玩家连接，当前在线：{len(self.connected_players)}")
          
    #       # 保持连接的关键循环
    #       while True:
    #           try:
    #               message = await websocket.recv()
    #               packet = GameProtocol.decode(message)
    #               if packet['type'] == MessageType.CONNECT:
    #                   print(f"玩家 {packet['data']['name']} 加入游戏")
                      
    #           except websockets.exceptions.ConnectionClosed:
    #               print("客户端正常断开连接")
    #               break
    #           except Exception as e:
    #               print(f"处理消息时发生异常: {str(e)}")
    #               break
                  
    #   finally:
    #       self.connected_players.discard(websocket)
    #       print(f"玩家断开，剩余连接：{len(self.connected_players)}")
        
    def _get_player_by_websocket(self, websocket):
        """通过WebSocket连接查找玩家名称"""
        for player, ws in self.connections.items():
            if ws == websocket:
                return player
        return None
        
    async def _send_to_player(self, player_name, msg_type, data):
        """向指定玩家发送消息"""
        if player_name in self.connections:
            await self.connections[player_name].send(
                GameProtocol.encode(msg_type, data)
            )

    async def _broadcast(self, room, msg_type, data):
        """向房间内所有玩家广播消息"""
        for player in room.players:
            await self._send_to_player(player, msg_type, data)

    async def _wait_for_action(self, player, timeout):
        """通过消息队列等待玩家动作"""
        try:
            # 获取对应玩家的WebSocket连接
            ws = self.connections[player]
            # 只处理当前玩家的消息
            while True:
                packet = await asyncio.wait_for(
                    self.message_queues[ws].get(),
                    timeout=timeout
                )
                if packet['type'] == MessageType.ACTION:
                    return packet['data']
        except asyncio.TimeoutError:
            return {'type': 'timeout'}
        
    # async def _game_loop(self, room):
    #     """游戏主循环（需要与之前代码衔接）"""
    #     while len(room.wall) > 0 and not room.game_over:
    #         current_player = room.players[room.current_player_index]
            
    #         # 摸牌阶段
    #         drawn_tile = room.wall.pop()
    #         await self._send_to_player(
    #             current_player,
    #             MessageType.DRAW_TILE,
    #             {"tile": drawn_tile}
    #         )
            
    #         # 等待玩家操作
    #         action = await self._wait_for_action(current_player, 30)
    #         await self._handle_player_action(room, current_player, action)
            
    #         # 切换玩家
    #         room.current_player_index = (room.current_player_index + 1) % 4
    #         await self._broadcast(
    #             room,
    #             MessageType.TURN_NOTIFY,
    #             {"current_player": room.current_player_index}
    #         )

    async def _handle_player_action(self, room, player, action):
        """处理玩家动作"""
        if action['type'] == 'discard':
            # 记录弃牌并广播
            room.discard_pile.append(action['tile'])
            await self._broadcast(
                room,
                MessageType.DISCARD,
                {
                    "player": player,
                    "tile": action['tile'],
                    "remaining": len(room.wall)
                }
            )


    # async def handle_client(self, websocket):
    #     try:
    #         async for message in websocket:
    #             packet = GameProtocol.decode(message)
    #             if packet['type'] == MessageType.CONNECT:
    #                 if 'name' not in packet['data']:
    #                     await websocket.close(code=1008, reason="Invalid connection request")
    #                     return
    #                 await self.handle_connect(websocket, packet['data'])
    #             elif packet['type'] == MessageType.ACTION:
    #                 print(f"收到动作消息: {packet['data']}")
    #                 # 添加实际动作处理逻辑
    #             elif packet['type'] == MessageType.HEARTBEAT:
    #                 print("收到心跳保持包")
    #             else:
    #                 print(f"未知消息类型: {packet['type']}")
    #     except websockets.ConnectionClosed as e:
    #         print(f"客户端断开连接，原因: {e.reason}")
            
    async def handle_client(self, websocket):
        """修复后的客户端处理方法"""
        print(f"新客户端连接: {websocket.remote_address}")
        self.message_queues[websocket] = asyncio.Queue()  # 预先初始化队列
        try:
            async for message in websocket:
                try:
                    # 增加心跳响应
                    # 只处理文本消息
                    if not isinstance(message, str):
                        print(f"收到非文本消息: {message}")
                        continue
                    print(f"收到原始消息: {message}")
                    try:
                        packet = GameProtocol.decode(message)
                        player_name = self._get_player_by_websocket(websocket)
                        
                        # 处理连接阶段消息
                        if not player_name and packet['type'] != MessageType.CONNECT:
                            await websocket.close(code=4003, reason="必须先发送CONNECT消息")
                            return
                        
                        # 将消息存入对应队列
                        await self.message_queues[websocket].put(packet)
                        
                        # 路由处理
                        await self.message_router(websocket, packet, player_name)
                        
                    except Exception as decode_error:
                        print(f"消息处理错误: {str(decode_error)}")
                        await websocket.close(code=1008, reason="Invalid message format")
                except Exception as decode_error:
                    print(f"消息处理错误: {str(decode_error)}")
                        
        except websockets.ConnectionClosed as e:
            print(f"连接关闭: {e.reason}")
        finally:
            # 修复KeyError
            player = self._get_player_by_websocket(websocket)
            if player:
                if player in self.connections:
                    del self.connections[player]
                if player in self.heartbeat_allowed:  # 新增检查
                    del self.heartbeat_allowed[player]

    async def handle_connect(self, ws, data):
        """增强的连接处理方法"""
        print(f"处理连接请求数据: {data}")  # 调试日志
        if 'name' not in data:
            print("缺少name字段，关闭连接")
            await ws.close(code=4000, reason="Missing name field")
            return
        
        player_name = data['name']
        print(f"玩家 {player_name} 尝试连接")
        
        # 检查重复连接
        if player_name in self.connections:
            print(f"玩家 {player_name} 已存在，拒绝重复连接")
            await ws.close(code=4001, reason="Duplicate player name")
            return
            
        # 分配房间
        try:
            room = await self.room_manager.assign_room(player_name)
            print(f"[DEBUG] 已分配房间: {room.room_id}")  # 新增日志
            self.connections[player_name] = ws
            print(f"玩家 {player_name} 成功加入房间 {room.room_id}")
            
            # 添加发送确认日志
            ack_data = {"status": "success", "room": room.room_id}
            print(f"[DEBUG] 发送连接确认: {ack_data}")  # 新增日志
            await ws.send(GameProtocol.encode(
                MessageType.CONNECT,
                ack_data
            ))
                
        except Exception as e:
            print(f"处理连接异常: {str(e)}")
            await ws.close(code=5000, reason="Server error")

    # 新增的start_game方法
    async def start_game(self, room):
        """开始游戏处理"""
        room.initialize_wall()
        room.deal_initial_tiles()
        room.status = 'playing'
        
        # 通知所有玩家游戏开始
        for idx, player in enumerate(room.players):
            await self._send_to_player(
                player,
                MessageType.GAME_START,
                {
                    "players": room.players,
                    "hand": room.hands[player],
                    "current_player": 0,  # 庄家先行
                    "wall_count": len(room.wall)
                }
            )
        
        # 启动游戏主循环
        await self._game_loop(room)

    async def _game_loop(self, room):
        """游戏主循环"""
        while not room.game_over and len(room.wall) > 0:
            current_player = room.players[room.current_player_index]
            
            # 1. 摸牌阶段
            drawn_tile = room.wall.pop()
            room.hands[current_player].append(drawn_tile)
            await self._send_to_player(
                current_player,
                MessageType.DRAW_TILE,
                {"tile": drawn_tile, "remaining": len(room.wall)}
            )
            
            # 2. 等待操作（30秒超时）
            try:
                action = await self._wait_for_action(current_player, timeout=30)
                if action['type'] == 'discard':
                    await self._process_discard(room, current_player, action['tile'])
            except asyncio.TimeoutError:
                print(f"玩家 {current_player} 操作超时，自动出牌")
                await self._auto_discard(room, current_player)
            
            # 3. 切换玩家
            room.current_player_index = (room.current_player_index + 1) % 4
            await self._broadcast(
                room,
                MessageType.TURN_NOTIFY,
                {"current_player": room.current_player_index}
            )
            
    async def _handle_player_action_by_websocket(self, websocket, data):
        """通过WebSocket处理玩家动作"""
        player = self._get_player_by_websocket(websocket)
        if player:
            room_id = self.room_manager.player_room_map.get(player)
            if room_id:
                room = self.room_manager.rooms[room_id]
                await self._handle_player_action(room, player, data)

    async def _process_discard(self, room, player, tile):
        """处理出牌"""
        # 从手牌移除
        if tile in room.hands[player]:
            room.hands[player].remove(tile)
        
        # 加入弃牌堆
        room.discard_pile.append({
            "player": player,
            "tile": tile,
            "timestamp": time.time()
        })
        
        # 广播弃牌事件
        await self._broadcast(
            room,
            MessageType.DISCARD,
            {
                "player": player,
                "tile": tile,
                "remaining": len(room.wall)
            }
        )

    async def start(self, port=8765):
        async with websockets.serve(self.handle_client, "0.0.0.0", port):
            print(f"服务器已启动，监听端口 {port}")
            await asyncio.Future()  # 永久运行

    async def message_router(self, websocket, packet, player):
        """统一消息路由"""
        try:
            if packet['type'] == MessageType.CONNECT:
                await self.handle_connect(websocket, packet['data'])
            elif packet['type'] == MessageType.HEARTBEAT:
                print(f"收到 {player} 的心跳包")
            elif packet['type'] == MessageType.ACTION:
                await self._handle_player_action_by_websocket(websocket, packet['data'])
            else:
                print(f"收到未处理消息类型: {packet['type']}")
        except Exception as e:
            print(f"消息路由错误: {str(e)}")

if __name__ == "__main__":
    #1. server = MahjongServer()
    # asyncio.run(server.start())

    server = MahjongServer()
    asyncio.run(server.start())