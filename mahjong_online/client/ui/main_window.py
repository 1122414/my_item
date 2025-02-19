# 界面组件
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsView, QLabel)
from PyQt5.QtCore import Qt, pyqtSignal,QObject
from .tile_widget import TileWidget

class MahjongWindow(QMainWindow):
    # def __init__(self, suit: str, value: str):
    def __init__(self,client):
        super().__init__()
        self.selected_tile_id = None  # 新增选中状态记录
        self.client = client
        self.controller = GameController(client)
        self.init_ui()
        # asyncio.create_task(self.start_message_loop())
        self.setWindowTitle("在线麻将")
        self.setGeometry(100, 100, 1280, 720)  # 窗口尺寸
        self.selected_tile = None  # 新增选中状态记录
        # self.suit = suit  # 必须包含suit属性
        # self.value = value  # 必须包含value属性

    async def start_message_loop(self):
        await self.client.receive_messages(self.controller)

    def init_ui(self):
        # 主容器
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        # 左侧信息面板
        info_panel = QVBoxLayout()
        self.status_label = QLabel("等待连接...")
        info_panel.addWidget(self.status_label)
        
        # 右侧游戏区域
        game_area = QVBoxLayout()
        
        # 其他玩家区域（上、对、下家）
        self.other_players = [
            self.create_player_panel("上家"),
            self.create_player_panel("对家"),
            self.create_player_panel("下家")
        ]
        
        # 中央牌桌
        self.table_view = QGraphicsView()
        self.table_view.setMinimumSize(600, 400)
        
        # 当前玩家手牌区
        self.hand_tiles_layout = QHBoxLayout()
        self.hand_tiles_widget = QWidget()
        self.hand_tiles_widget.setLayout(self.hand_tiles_layout)
        
        # 组装游戏区域
        game_area.addWidget(self.other_players[0])
        game_area.addWidget(self.table_view)
        game_area.addWidget(self.other_players[1])
        game_area.addWidget(self.hand_tiles_widget)
        game_area.addWidget(self.other_players[2])
        
        main_layout.addLayout(info_panel, 1)
        main_layout.addLayout(game_area, 4)
        
        self.setCentralWidget(main_widget)
        self.controller.turn_started.connect(self.handle_turn_start)
        self.controller.state_updated.connect(self.update_state)

    def create_player_panel(self, name):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))
        self.discard_area = QHBoxLayout()  # 弃牌区
        layout.addLayout(self.discard_area)
        panel.setLayout(layout)
        return panel

    def update_hand_tiles(self, tiles):
        """更新手牌显示"""
        # 清空现有手牌
        while self.hand_tiles_layout.count():
            child = self.hand_tiles_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # 添加新牌
        for tile in tiles:
            tile_widget = TileWidget(tile)
            tile_widget.clicked.connect(self.on_tile_click)
            self.hand_tiles_layout.addWidget(tile_widget)

    def on_tile_click(self, tile_id):
        """处理牌点击事件"""
        # 取消之前选中的牌
        if self.selected_tile_id:
            for i in range(self.hand_tiles_layout.count()):
                widget = self.hand_tiles_layout.itemAt(i).widget()
                if widget.tile_id == self.selected_tile_id:
                    widget.set_selected(False)
        
        # 切换选中状态
        if self.selected_tile_id == tile_id:
            self.selected_tile_id = None
            print("取消选中所有牌")
        else:
            self.selected_tile_id = tile_id
            print(f"选中牌: {tile_id}")
            # 设置新选中的牌
            for i in range(self.hand_tiles_layout.count()):
                widget = self.hand_tiles_layout.itemAt(i).widget()
                widget.set_selected(widget.tile_id == tile_id)
    def handle_turn_start(self, data):
        self.status_label.setText(f"轮到您操作，剩余牌: {data['remaining']}")
        if self.client.current_turn:
            self.draw_tile_animation()

    def draw_tile_animation(self):
        # 摸牌动画效果
        new_tile = self.client.hand[-1]
        tile_widget = TileWidget(new_tile)
        tile_widget.setGeometry(800, 100, 60, 90)
        tile_widget.show()
        # 实现动画移动到手牌区...

    def update_state(self, data):
        self.status_label.setText(f"当前操作玩家: {data['current_player']}")

class GameController(QObject):
    game_started = pyqtSignal(dict)
    turn_started = pyqtSignal(dict)
    state_updated = pyqtSignal(dict)

    def __init__(self, client):
        super().__init__()
        self.client = client

    def on_game_start(self, data):
        self.game_started.emit(data)

    def on_turn_start(self, data):
        self.turn_started.emit(data)

    def update_game_state(self, data):
        self.state_updated.emit(data)