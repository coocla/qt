#coding:utf-8 
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

from cloudtea.widgets import base, components, status


class SideBarPanel(base.TFrame):
    def __init__(self, app, parent=None):
        super(SideBarPanel, self).__init__(parent)
        self._app = app

        self.header = base.TGroupHeader(self._app, u'管理中心')
        self.current_side_item = base.TGroupItem(self._app, u'桌面')
        self.current_side_item.set_img_text('❂')
        self._layout = QVBoxLayout(self)

        self.setObjectName('lp_library_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = ''' 
            #{0} {{ 
                background: transparent; 
            }} 
         '''.format(self.objectName(), 
            theme.color3.name())
        self.setStyleSheet(style_str) 

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addSpacing(8)
        self._layout.addWidget(self.header)
        self._layout.addWidget(self.current_side_item)

    def add_item(self, item):
        self._layout.addWidget(item)


class TopPanel(base.TFrame):
    def __init__(self, app, parent=None):
        super(TopPanel, self).__init__(parent)
        self._app = app

        self._layout = QHBoxLayout(self)
        self.setObjectName('pc_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme 
        style_str = ''' 
            #{0} {{ 
                background: transparent; 
                color: {1}; 
                border-bottom: 3px inset {3}; 
            }} 
        '''.format(self.objectName(), 
                   theme.foreground.name(), 
                   theme.color0_light.name(), 
                   theme.color0_light.name()) 
        self.setStyleSheet(style_str) 


    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setFixedHeight(50)
        self._layout.addSpacing(5)

    def add_item(self, widget):
        self._layout.addWidget(widget)
        self._layout.addStretch(1)



class LeftPanel(base.TFrame):
    def __init__(self, app, parent=None):
        super(LeftPanel, self).__init__(parent)
        self._app = app

        self._layout = QVBoxLayout(self)
        self.sidebar_panel = SideBarPanel(self._app)
        self.setLayout(self._layout)
        self.setObjectName('c_left_panel')

        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
            }}
        '''.format(self.objectName(),
                   theme.color5.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._layout.addWidget(self.sidebar_panel)
        self._layout.addStretch(1)
         
        # 这是测试时用的
        #a = base.TGroupItem(self._app, u'哈哈')
        #self.sidebar_panel.add_item(a)

class LeftPanel_Container(base.TScrollArea):
    def __init__(self, app, parent=None):
        super(LeftPanel_Container, self).__init__(parent)
        self._app = app

        self.left_panel = LeftPanel(self._app)
        self._layout = QVBoxLayout(self)
        self.setWidget(self.left_panel)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setObjectName('c_left_panel_container')
        self.set_theme_style()
        self.setMinimumWidth(80)
        self.setMaximumWidth(160)

        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                border: 0px;
                border-right: 3px inset {1};
            }}
        '''.format(self.objectName(),
                   theme.color0_light.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)


class RightPanel(base.TFrame):
    def __init__(self, app, parent=None):
        super(RightPanel, self).__init__(parent)
        self._app = app

        self.widget = None
        self._layout = QVBoxLayout(self)
        self.setLayout(self._layout)
        self.setObjectName('right_panel')

        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        style_str = '''
            #{0} {{
                background: transparent;
                padding: 20px 30px 0px 30px;
            }}
        '''.format(self.objectName())
        self.setStyleSheet(style_str)

    def set_widget(self, widget):
        if self.widget and self.widget != widget:
            self._layout.removeWidget(self.widget)
            self.widget.hide()
            widget.show()
            self._layout.addWidget(widget)
        else:
            self._layout.addWidget(widget)
        self.widget = widget

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

class RightPanel_Container(base.TScrollArea):
    def __init__(self, app, parent=None):
        super(RightPanel_Container, self).__init__(parent)
        self._app = app

        self.right_panel = RightPanel(self._app)
        self._layout = QVBoxLayout(self)
        self.setWidget(self.right_panel)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setObjectName('c_left_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                border: 0px;
            }}
        '''.format(self.objectName(),
                   theme.color5.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)


class CentralPanel(base.TFrame):
    def __init__(self, app, parent=None):
        super(CentralPanel, self).__init__(parent)
        self._app = app

        self.top_panel = TopPanel(self._app, self)
        self.right_panel_container = RightPanel_Container(self._app, self)
        #self.left_panel = self.left_panel_container.left_panel
        self.right_panel = self.right_panel_container.right_panel

        self._layout = QVBoxLayout(self)
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        style_str = '''
            #{0} {{
                background: transparent;
            }}
        '''.format(self.objectName())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._layout.addWidget(self.top_panel)
        self._layout.addWidget(self.right_panel_container)

class StatusPanel(base.TFrame):
    def __init__(self, app, parent=None):
        super(StatusPanel, self).__init__(parent)
        self._app = app
        self._layout = QHBoxLayout(self)

        self.network_status_label = status.NetworkStatus(self._app)
        self.message_label = status.MessageLabel(self._app)
        self.theme_switch_btn = status.ThemeComboBox(self._app, self)

        self.setup_ui()
        self.setObjectName('status_panel')
        self.set_theme_style()

    def setup_ui(self):
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)
        self.setFixedHeight(18)

        self._layout.addWidget(self.network_status_label)
        self._layout.addStretch(0)
        self._layout.addWidget(self.message_label)
        self._layout.addStretch(0)
        self._layout.addWidget(self.theme_switch_btn)

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
            }}
        '''.format(self.objectName(),
                theme.color0.name())
        self.setStyleSheet(style_str)


class UI(object):
    def __init__(self, app):
        self._box = QHBoxLayout()
        self._layout = QVBoxLayout(app)
        self.side_panel = LeftPanel_Container(app, app)
        self.central_panel = CentralPanel(app, app)
        self.current_desktop = components.RoomTable(app)
        self.status_panel = StatusPanel(app, app)
        self.setup_ui()

    def setup_ui(self):
        self._box.setContentsMargins(0, 0, 0, 0)
        self._box.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._box.addWidget(self.side_panel)
        self._box.addWidget(self.central_panel)
        self._layout.addLayout(self._box)
        self._layout.addWidget(self.status_panel)

