from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QGraphicsScene, QGraphicsView
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter
import qasync
import asyncio


class MahjongWindow(QMainWindow):
    update_signal = pyqtSignal(dict)  # 用于跨线程更新UI的信号

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        """初始化主界面"""
        self.setWindowTitle("在线麻将 - 玩家: " + self.client.player_name)
        self.setGeometry(100, 100, 1200, 800)

        # 主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # 游戏信息面板
        self.info_panel = QLabel("等待游戏开始...")
        main_layout.addWidget(self.info_panel)

        # 玩家手牌区域
        self.hand_panel = QGraphicsView()
        self.hand_scene = QGraphicsScene()
        self.hand_panel.setScene(self.hand_scene)
        main_layout.addWidget(self.hand_panel)

        # 弃牌区
        self.discard_panel = QGraphicsView()
        self.discard_scene = QGraphicsScene()
        self.discard_panel.setScene(self.discard_scene)
        main_layout.addWidget(self.discard_panel)

        # 操作按钮
        self.action_panel = QWidget()
        action_layout = QHBoxLayout()
        self.discard_btn = QPushButton("出牌")
        self.pong_btn = QPushButton("碰")
        self.kong_btn = QPushButton("杠") 
        self.hu_btn = QPushButton("胡")
        action_layout.addWidget(self.discard_btn)
        action_layout.addWidget(self.pong_btn)
        action_layout.addWidget(self.kong_btn)
        action_layout.addWidget(self.hu_btn)
        self.action_panel.setLayout(action_layout)
        main_layout.addWidget(self.action_panel)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def connect_signals(self):
        """连接信号与槽"""
        self.update_signal.connect(self.on_update)
        self.discard_btn.clicked.connect(self.on_discard)

    def on_update(self, packet):
        """更新游戏状态"""
        if packet['type'] == 'GAME_START':
            self.show_game_start(packet['data'])
        elif packet['type'] == 'PRIVATE_HAND':
            self.update_hand(packet['data'])
        elif packet['type'] == 'DISCARD':
            self.update_discard(packet['data'])

    def show_game_start(self, data):
        """显示游戏开始界面"""
        players = data['players']
        self.info_panel.setText(f"游戏开始！玩家: {', '.join(players)}")

    def update_hand(self, data):
        """更新手牌显示"""
        self.hand_scene.clear()
        tile_size = 60
        for i, tile in enumerate(data['hand']):
            pixmap = self._get_tile_image(tile)
            item = self.hand_scene.addPixmap(pixmap)
            item.setPos(i * tile_size, 0)
            item.setData(0, tile)  # 存储牌面数据

    def update_discard(self, data):
        """更新弃牌区"""
        self.discard_scene.clear()
        tile_size = 40
        for i, item in enumerate(data['discards']):
            pixmap = self._get_tile_image(item['tile'], small=True)
            self.discard_scene.addPixmap(pixmap).setPos(
                (i % 10) * tile_size, 
                (i // 10) * tile_size
            )

    def _get_tile_image(self, tile, small=False):
        """获取牌面图片（需要准备图片资源）"""
        size = (80, 120) if not small else (40, 60)
        # 这里需要实际图片文件路径，示例使用占位图
        pixmap = QPixmap(size[0], size[1])
        pixmap.fill(Qt.GlobalColor.white)
        painter = QPainter(pixmap)
        painter.drawText(10, 20, tile)
        painter.end()
        return pixmap

    def on_discard(self):
        """出牌按钮点击处理"""
        selected = self.hand_panel.scene().selectedItems()
        if selected:
            tile = selected[0].data(0)
            self.client.send_action({'type': 'discard', 'tile': tile})

async def run_with_ui(client):
    """带UI运行客户端"""
    app = qasync.QApplication.instance() or qasync.QApplication([])
    window = MahjongWindow(client)
    window.show()

    # 创建独立的事件循环任务
    loop = asyncio.get_event_loop()
    ui_task = loop.create_task(app.exec())
    msg_task = loop.create_task(message_loop(client))

    await asyncio.gather(ui_task, msg_task)
    
    async def message_loop():
        while client._running:
            await client.process_messages()
            await asyncio.sleep(0.1)
    
    # await asyncio.gather(
    #     message_loop(),
    #     app.exec()
    # )