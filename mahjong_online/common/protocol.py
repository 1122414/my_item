# 网络协议# common/protocol.py
from enum import Enum
import json

class MessageType(Enum):
    CONNECT = 1
    ACTION = 2
    GAME_STATE = 3
    HEARTBEAT = 4  # 新增心跳类型

class GameProtocol:
    @staticmethod
    def encode(msg_type: MessageType, data: dict):
        return json.dumps({
            "type": msg_type.value,
            "data": data
        }).encode('utf-8')

    @staticmethod
    def decode(data: bytes):
        packet = json.loads(data.decode('utf-8'))
        packet["type"] = MessageType(packet["type"])
        return packet