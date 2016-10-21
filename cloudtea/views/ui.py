#coding:utf-8 
from PySide.QtGui import QVBoxLayout, QHBoxLayout
from PySide.QtCore import Qt
from cloudtea.widgets import base


class SideBarPanel(base.TFrame):
    def __init__(self, app, parent=None):
        super(SideBarPanel, self).__init__(parent)
        self._app = app

        self.header = base.TGroupHeader(self._app, u'管理中心')
        self._layout = QVBoxLayout(self)
        self.setObjectName('func_list_panel')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        pass

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.header)

    def add_item(self, item):
        self._layout.addWidget(item)


class TopPanel(base.TFrame):
    def __init__(self, app, parent=None):
        super(TopPanel, self).__init__(parent)
        self._app = app

        self._layout = QHBoxLayout(self)
        self.setLayout(self._layout)
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        pass

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setFixedHeight(50)
        self._layout.addSpacing(5)



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
        self.setMinimumWidth(180)
        self.setMaximumWidth(220)

        self.set_theme_style()
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

        self.left_panel_container = LeftPanel_Container(self._app, self)
        self.right_panel_container = RightPanel_Container(self._app, self)
        self.left_panel = self.left_panel_container.left_panel
        self.right_panel = self.right_panel_container.right_panel

        self._layout = QHBoxLayout(self)
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

        self._layout.addWidget(self.left_panel_container)
        self._layout.addWidget(self.right_panel_container)


class UI(object):
    def __init__(self, app):
        self._layout = QVBoxLayout(app)
        self.top_panel = TopPanel(app, app)
        self.central_panel = CentralPanel(app, app)
        #self.central_panel.right_panel.set_widget()
        self.setup_ui()

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.top_panel)
        self._layout.addWidget(self.central_panel)

