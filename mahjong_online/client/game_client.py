# 网络客户端# client/game_client.py 基础客户端
import asyncio
import websockets
from common.protocol import GameProtocol, MessageType

class GameClient:
    def __init__(self, player_name):
        self.websocket = None
        self.name = player_name

    async def connect(self):
        self.websocket = await websockets.connect("ws://localhost:8765")
        await self.send(MessageType.CONNECT, {"name": self.name})

    async def send(self, msg_type, data):
        await self.websocket.send(GameProtocol.encode(msg_type, data))

async def main():
    client = GameClient("测试玩家")
    try:
        await client.connect()
        print("已连接到服务器")
        
        # 保持连接的心跳机制
        while True:
            await asyncio.sleep(5)  # 每5秒发送心跳
            await client.send(MessageType.ACTION, {"type": "heartbeat"})
            
    except KeyboardInterrupt:
        print("主动断开连接")
    except Exception as e:
        print(f"连接异常: {str(e)}")
    finally:
        await client.websocket.close()

if __name__ == "__main__":
    asyncio.run(main())