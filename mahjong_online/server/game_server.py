# 主服务程序# server/game_server.py 完整代码
import asyncio
import websockets
from common.protocol import GameProtocol, MessageType

class MahjongServer:
    def __init__(self):
        self.connected_players = set()

    async def handle_client(self, websocket):
      try:
          self.connected_players.add(websocket)
          print(f"新玩家连接，当前在线：{len(self.connected_players)}")
          
          # 保持连接的关键循环
          while True:
              try:
                  message = await websocket.recv()
                  packet = GameProtocol.decode(message)
                  if packet['type'] == MessageType.CONNECT:
                      print(f"玩家 {packet['data']['name']} 加入游戏")
                      
              except websockets.exceptions.ConnectionClosed:
                  print("客户端正常断开连接")
                  break
              except Exception as e:
                  print(f"处理消息时发生异常: {str(e)}")
                  break
                  
      finally:
          self.connected_players.discard(websocket)
          print(f"玩家断开，剩余连接：{len(self.connected_players)}")

    async def start(self, port=8765):
        async with websockets.serve(self.handle_client, "0.0.0.0", port):
            print(f"服务器已启动，监听端口 {port}")
            await asyncio.Future()  # 永久运行

if __name__ == "__main__":
    server = MahjongServer()
    asyncio.run(server.start())