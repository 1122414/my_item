# 网络客户端# client/game_client.py 基础客户端
import time
import asyncio
import argparse  # 新增命令行解析库
import websockets
from client.ui.main_window import run_with_ui
from common.protocol import GameProtocol, MessageType

class GameClient:
    def __init__(self, player_name):
        self.player_name = player_name  # 初始化属性
        self.websocket = None
        self._running = True  # 新增初始化属性
        self.hand = []
        self.current_turn = -1
        self.message_queue = asyncio.Queue()  # 新增消息队列

    async def connect(self):
        """修复后的连接方法"""
        # 增加连接超时时间到30秒
        self.websocket = await websockets.connect(
            "ws://localhost:8765",
            open_timeout=30  # 新增连接超时设置
        )
        asyncio.create_task(self._listen_task())  # 启动单一监听任务
        
        # 发送连接请求
        await self.send(MessageType.CONNECT, {"name": self.player_name})
        
        # 通过消息队列等待连接确认
        try:
            ack = await asyncio.wait_for(
                self._wait_for_ack(),
                timeout=10
            )
            if not ack['data'].get('status') == 'success':
                raise ConnectionError(ack['data'].get('reason', '未知错误'))
        except asyncio.TimeoutError:
            raise ConnectionError("连接超时")
        
    async def _wait_for_ack(self):
        """通过消息队列等待连接确认"""
        while self._running:
            try:
                message = await asyncio.wait_for(
                    self.message_queue.get(),
                    timeout=0.5
                )
                packet = GameProtocol.decode(message)
                if packet['type'] == MessageType.CONNECT:
                    return packet
            except asyncio.TimeoutError:
                continue
        raise ConnectionError("连接中断")

    async def _listen_task(self):
        """优化后的心跳处理"""
        try:
            while self._running:
                try:
                    # 设置更短的心跳超时
                    message = await asyncio.wait_for(
                        self.websocket.recv(),
                        timeout=15  # 调整为15秒
                    )
                    await self.message_queue.put(message)
                except asyncio.TimeoutError:
                    if self._running:
                        await self.send(MessageType.HEARTBEAT, {"ts": time.time()})
        except Exception as e:
            print(f"监听异常: {str(e)}")
        finally:
            self._running = False



    async def process_messages(self):
        """处理消息队列"""
        while self._running:
            try:
                message = await asyncio.wait_for(
                    self.message_queue.get(),
                    timeout=0.1
                )
                await self._handle_message(message)
            except asyncio.TimeoutError:
                continue

    async def heartbeat_loop(self):
        """安全的心跳循环"""
        while self._running:
            await asyncio.sleep(5)
            await self.send(MessageType.HEARTBEAT, {"timestamp": time.time()})

    async def send(self, msg_type, data):
        await self.websocket.send(GameProtocol.encode(msg_type, data))

    async def listen(self):
        """消息监听循环（必须放在GameClient类中）"""
        try:
            while self._running:
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=30)
                    await self._handle_message(message)
                except asyncio.TimeoutError:
                    await self.send(MessageType.HEARTBEAT, {})
        except websockets.ConnectionClosed:
            print("连接已关闭")
        finally:
            self._running = False

    # async def _handle_message(self, message):
    #     packet = GameProtocol.decode(message)
    #     if packet['type'] == MessageType.GAME_START:
    #         self.game_state.hand = packet['data']['hand']  # 更新手牌
    #         self.game_state.players = packet['data']['players']
    #         self.ui.update_hand_tiles()  # 刷新UI手牌显示
            
    async def _handle_message(self, message):
        packet = GameProtocol.decode(message)
        print(f"\n=== 收到 {packet['type']} 消息 ===")  # 显示具体消息类型
        
        try:
            if packet['type'] == MessageType.GAME_START:
                print(f"游戏开始！玩家列表: {', '.join(packet['data']['players'])}")
                print(f"初始牌墙剩余: {packet['data']['wall_count']}张")

            elif packet['type'] == MessageType.PRIVATE_HAND:
                self.hand = packet['data']['hand']
                self.hand.sort(key=lambda x: (self._suit_order(x), self._tile_value(x)))
                print("\n你的手牌:")
                self._print_formatted_hand()
                if packet['data']['is_dealer']:
                    print("★ 您是庄家")

            elif packet['type'] == MessageType.DRAW_TILE:
                new_tile = packet['data']['tile']
                print(f"\n摸牌 → {new_tile}")
                self.hand.append(new_tile)
                self.hand.sort(key=lambda x: (self._suit_order(x), self._tile_value(x)))
                self._print_formatted_hand()

            elif packet['type'] == MessageType.DISCARD:
                player = packet['data']['player']
                tile = packet['data']['tile']
                remaining = packet['data']['remaining']
                print(f"\n{player} 打出 {tile}")
                print(f"牌墙剩余: {remaining}张")

            elif packet['type'] == MessageType.TURN_NOTIFY:
                current_player = packet['data']['current_player']
                if current_player == self.player_name:
                    print("\n★★★ 轮到您操作了！请输入要打出的牌 ★★★")
                else:
                    print(f"\n等待 {current_player} 操作...")

            elif packet['type'] == MessageType.PONG_NOTIFY:
                print(f"\n{packet['data']['player']} 进行了碰牌")

            elif packet['type'] == MessageType.GAME_OVER:
                winner = packet['data']['winner']
                print(f"\n🎉 游戏结束！胜者: {winner} 🎉")

            else:
                print(f"未处理的消息类型: {packet['type']}")

        except Exception as e:
            print(f"消息处理错误: {str(e)}")

    def _suit_order(self, tile):
        """花色排序辅助函数"""
        if '万' in tile: return 0
        if '筒' in tile: return 1
        if '条' in tile: return 2
        return 3  # 字牌

    def _tile_value(self, tile):
        """牌面值排序辅助函数"""
        if tile[0].isdigit():
            return int(tile[0])
        return 0  # 字牌按出现顺序排列

    def _print_formatted_hand(self):
        """按花色分组格式化打印手牌"""
        suits = {'万': [], '筒': [], '条': [], '字': []}
        for tile in self.hand:
            if '万' in tile: suits['万'].append(tile)
            elif '筒' in tile: suits['筒'].append(tile)
            elif '条' in tile: suits['条'].append(tile)
            else: suits['字'].append(tile)
        
        for suit, tiles in suits.items():
            if tiles:
                print(f"{suit}: {' '.join(sorted(tiles, key=self._tile_value))}")
        print()

    async def close(self):
        """关闭连接"""
        self._running = False
        if self.websocket:
            await self.websocket.close()

# 修改main函数
async def main():
    parser = argparse.ArgumentParser(description='麻将客户端')
    parser.add_argument('name', type=str, help='玩家名称', default="玩家1", nargs='?')
    args = parser.parse_args()
    
    client = GameClient(args.name)
    try:
        await client.connect()
        # 启动UI版本
        # from ui.main_window import run_with_ui
        await run_with_ui(client)
            
    except KeyboardInterrupt:
        print("主动断开连接")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())