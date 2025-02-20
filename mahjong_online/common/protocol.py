# common/protocol.py
from enum import Enum
import json

class ProtocolError(Exception):
    pass

class MessageType(Enum):
    CONNECT = 1
    GAME_START = 2
    ACTION = 3
    HEARTBEAT = 4
    DISCARD = 5
    GAME_OVER = 6
    DRAW_TILE = 7
    TURN_NOTIFY = 8
    PRIVATE_HAND = 9  # 私有手牌

class GameProtocol:
    

    @staticmethod
    def encode(msg_type: MessageType, data: dict):
        return json.dumps({
            "type": msg_type.value,
            "data": data
        }).encode('utf-8')

    @staticmethod


    def decode(data: bytes):
        try:
            packet = json.loads(data.decode('utf-8'))
            if "type" not in packet or "data" not in packet:
                raise ValueError("Invalid packet format")
                
            packet["type"] = MessageType(packet["type"])  # 可能触发ValueError
            return packet
        except (json.JSONDecodeError, ValueError) as e:
            raise ProtocolError(f"协议解析失败: {str(e)}")
    
