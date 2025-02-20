from enum import Enum

class Suit(Enum):
    """麻将花色枚举"""
    WAN = '万'    # 万
    TONG = '筒'   # 筒
    TIAO = '条'   # 条
    HONORS = '字' # 字牌

TILE_COUNTS = {
    Suit.WAN: 9,    # 万：1-9各4张
    Suit.TONG: 9,   # 筒：1-9各4张
    Suit.TIAO: 9,   # 条：1-9各4张
    Suit.HONORS: 7  # 字牌：东南西北中发白
}