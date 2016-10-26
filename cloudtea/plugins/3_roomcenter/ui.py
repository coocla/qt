#coding:utf-8
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem

from cloudtea.widgets import base, components

class Input(base.TLineEdit):
    def __init__(self, app, tiptext=None, parent=None):
        super(Input, self).__init__(parent)
        self._app = app
        self.setObjectName('input')
        self.setPlaceholderText(tiptext)
        self.set_theme_style()

    def set_theme_style(self):
        style_str = '''
            #{0} {{
                background-color: #ffffff;
                border: 1px solid #e5e6e7;
                color: inherit;
                width: 300px;
                height: 30px;
            }}
            #{0}::focus {{
                border-color: #39adb4;
            }}
        '''.format(self.objectName())
        self.setStyleSheet(style_str)


class NewRoom(base.TDialog):
    def __init__(self, app, parent=None):
        super(NewRoom, self).__init__(parent)
        self._app = app
        self.setObjectName('modal')
        self._layout = QVBoxLayout(self)
        self.box = QVBoxLayout()

        self.room_name = Input(self, u'房间名')
        self.room_vip_price = Input(self, u'会员房费, 单位: 元')
        self.room_common_price = Input(self, u'普通顾客房费, 单位: 元')
        self.room_capacity = Input(self, u'房间可容纳人数, 单位: 位')
        self.ok_btn = base.TLButton(self._app, u'提交', size=19)

        self.head = components.ModalHeader(self._app, self)
        self.body = components.ModalBody(self._app, self)
        self.foot = components.ModalFooter(self._app, self)

        self.set_theme_style()
        self.setup_ui()

    def setup_ui(self):
        self.resize(800, 500)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.head)
        self._layout.addWidget(self.body)
        self._layout.addWidget(self.foot)
        
        self.box.setContentsMargins(0,0,0,0)
        self.box.setSpacing(0)
        self.box.addSpacing(15)
        self.box.addWidget(self.room_name)
        self.box.addSpacing(20)
        self.box.addWidget(self.room_vip_price)
        self.box.addSpacing(20)
        self.box.addWidget(self.room_common_price)
        self.box.addSpacing(20)
        self.box.addWidget(self.room_capacity)
        self.box.addStretch(1)

        self.head.set_header(u'增加房间')
        self.foot.add_item(self.ok_btn)
        self.body.add_item()
        self.body.add_item(self.box)
        self.body.add_item()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme 
        style_str = '''
            #{0} {{ 
                background: {1}; 
                color: {2}; 
            }} 
        '''.format(self.objectName(), 
                   theme.background.name(), 
                   theme.foreground.name()) 
        self.setStyleSheet(style_str)



class UI(object):
    def __init__(self, app):
        self._app = app

        #初始化创建窗口
        self.newroom_dialog = NewRoom(self._app, self._app)

        self.room_item = base.TGroupItem(self._app, u'房间管理')
        self.room_item.set_img_text('>')

        #创建按钮
        self.refresh_btn = base.TLButton(self._app, u'刷新')
        self.newroom_btn = base.TLButton(self._app, u'新增房间')
        self.delroom_btn = base.TLButton(self._app, u'删除房间')
        self.setup_ui()

    def setup_ui(self):
        side_panel = self._app.ui.side_panel.left_panel
        # 创建桌面对象
        self.desktop = components.RoomTable(self._app)
        # 创建侧边菜单
        side_panel.sidebar_panel.add_item(self.room_item)