# 游戏逻辑# client/logic/mahjong.py 补充测试代码
import random
import unittest

class MahjongTile:
    def __init__(self, suit: str, value: str):
        self.suit = suit  # 万/筒/条/字
        self.value = value
    
    def __repr__(self):
        return f"{self.value}{self.suit.value if self.suit != Suit.HONORS else ''}"
    
    #1. def get_id(self):
    #     """生成唯一牌标识"""
    #     if self.suit == '字':
    #         return f"{self.value}"
    #     return f"{self.value}{self.suit}"

class Wall:
    def __init__(self):
        self.tiles = self._generate_wall()
    
    def _generate_wall(self):
        tiles = []
        # for suit in Suit:
        #     if suit == Suit.HONORS:
        #         for h in ['东','南','西','北','中','发','白']:
        #             tiles += [MahjongTile(suit, h) for _ in range(4)]
        #     else:
        #         for n in range
        # 生成数牌（万/筒/条）
        for suit in ['万', '筒', '条']:
            for num in range(1, 10):
                tiles += [MahjongTile(suit, str(num))] * 4
        # 生成字牌
        for honor in ['东','南','西','北','中','发','白']:
            tiles += [MahjongTile('字', honor)] * 4
        random.shuffle(tiles)
        return tiles

# 测试用例
class TestMahjong(unittest.TestCase):
    def test_wall_generation(self):
        wall = Wall()
        self.assertEqual(len(wall.tiles), 136)
        self.assertEqual(len([t for t in wall.tiles if t.suit == '万']), 36)
        self.assertEqual(len([t for t in wall.tiles if t.value == '东']), 4)

if __name__ == "__main__":
    unittest.main()