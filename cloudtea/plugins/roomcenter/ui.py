#coding:utf-8
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy

from cloudtea.widgets import base

class Input(base.TLineEdit):
    def __init__(self, app, parent=None):
        super(Input, self).__init__(parent)
        self._app = app
        self.setObjectName('input')
        self.set_theme_style()

    def set_theme_style(self):
        pass


class CreateButton(base.TLabel):
    clicked = pyqtSignal()

    def __init__(self, app, text=None, parent=None):
        super(CreateButton, self).__init__()
        self._app = app
        print(self._app)
        self.setText(u'新增')
        self.setToolTip(u'新增房间')
        self.setObjectName('room_create_btn')
        self.set_theme_style()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = ''' 
            #{0} {{
                background: transparent;
                color: {1};
            }}
            #{0}:hover {{
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.foreground.name(),
                   theme.color4.name())
        self.setStyleSheet(style_str)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()

class CreateDialog(base.TDialog):
    def __init__(self, app, parent=None):
        super(CreateDialog, self).__init__(parent)
        self._app = app
        self.room_name = Input(self)
        self.room_vip_price = Input(self)
        self.room_common_price = Input(self)
        self.room_capacity = Input(self)
        self.ok_btn = base.TButton(u'创建', self)
        self._layout = QVBoxLayout(self)

        self.room_name.setPlaceholderText(u'房间名')
        self.room_vip_price.setPlaceholderText(u'VIP客户房费')
        self.room_common_price.setPlaceholderText(u'普通客户房费')
        self.room_capacity.setPlaceholderText(u'房间可容纳人数')

        self.setObjectName('login_dialog')
        self.set_theme_style()
        self.setup_ui()

        self.room_name.textChanged.connect(self.verify_name)

    def set_theme_style(self):
        pass

    def setup_ui(self):
        self.setFixedWidth(200)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._layout.addWidget(self.room_name)
        self._layout.addWidget(self.room_vip_price)
        self._layout.addWidget(self.room_common_price)
        self._layout.addWidget(self.room_capacity)
        self._layout.addWidget(self.ok_btn)

    def verify_name(self, text):
        print('verify_name is %s' % text)



class UI(object):
    def __init__(self, app):
        self._app = app

        #初始化创建窗口
        self.create_dialog = CreateDialog(self._app, self._app)
        #创建按钮
        self.create_btn = CreateButton(self._app)
        # self.menu_container = base.TFrame()

        self.room_item = base.TGroupItem(self._app, u'房间管理')
        self.room_item.set_img_text('>')
        self.bind_signal()
        # self._menu_layout = QHBoxLayout(self.menu_container)

        self.setup_ui()

    def setup_ui(self):
        # self._menu_layout.setContentsMargins(0, 0, 0, 0)
        # self._menu_layout.setSpacing(0)
        # self._menu_layout.addWidget(self.create_btn)
        self.create_btn.setFixedSize(30, 30)
        top_panel = self._app.ui.central_panel.top_panel
        side_panel = self._app.ui.side_panel.left_panel

        top_panel.add_item(self.create_btn)
        side_panel.sidebar_panel.add_item(self.room_item)

    def bind_signal(self):
        self.room_item.clicked.connect(self._app.switch_desktop)