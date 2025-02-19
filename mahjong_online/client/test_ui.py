import sys
from PyQt5.QtWidgets import QApplication
from client.ui.main_window import MahjongWindow
from client.logic.mahjong import MahjongTile

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 生成测试手牌
    test_tiles = [
        MahjongTile('万', '1'),
        MahjongTile('筒', '5'),
        MahjongTile('条', '9'),
        MahjongTile('字', '东'),
        MahjongTile('万', '3')
    ]
    
    window = MahjongWindow()
    window.update_hand_tiles(test_tiles)
    window.show()
    
    sys.exit(app.exec_())