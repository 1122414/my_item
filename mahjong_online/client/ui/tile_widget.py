from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QPixmap, QFont, QColor, QPen
from PyQt5.QtCore import Qt, pyqtSignal

class TileWidget(QWidget):
    clicked = pyqtSignal(str)  # 点击信号传递牌面值
    
    def __init__(self, tile_data, parent=None):
        super().__init__(parent)
        self.tile_data = tile_data
        self.is_selected = False
        self.tile_id = f"{self.tile_data.suit}_{self.tile_data.value}"  # 新增ID属性
        self.setFixedSize(60, 90)

    def set_selected(self, selected):
        """外部控制选中状态"""
        self.is_selected = selected
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        # 绘制牌面背景（根据选中状态改变颜色）
        if self.is_selected:
            painter.setBrush(QColor(173, 216, 230))  # 浅蓝色
        else:
            painter.setBrush(Qt.white)
            
        painter.drawRoundedRect(0, 0, 60, 90, 5, 5)
        
        # 显示牌面文字
        font = QFont("Arial", 20)
        painter.setFont(font)
        # if self.tile.suit == '字':
        #     text = self.tile.value
        # else:
        #     text = f"{self.tile.value}\n{self.tile.suit}"

        # 在绘制时也使用tile_data
        text = f"{self.tile_data.value}\n{self.tile_data.suit}" if self.tile_data.suit != '字' else self.tile_data.value
            
        painter.drawText(self.rect(), Qt.AlignCenter, text)
        
         # 选中状态边框（加粗）
        if self.is_selected:
            painter.setPen(QPen(Qt.red, 3))  # 3像素宽的红边
            painter.drawRoundedRect(3, 3, 54, 84, 5, 5)  # 调整位置防止溢出

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 不再自己维护状态，只发送信号
            self.clicked.emit(self.tile_id)
        else:
            super().mousePressEvent(event)

    # def mousePressEvent(self, event):
        # if event.button() == Qt.LeftButton:
        #     self.is_selected = not self.is_selected
        #     self.update()
        #     # 正确访问tile_data的属性
        #     tile_id = f"{self.tile_data.suit}_{self.tile_data.value}"
        #     self.clicked.emit(tile_id)
        # else:
        #     super().mousePressEvent(event)