#coding:utf-8
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QWidgetItem
from PyQt5.QtCore import Qt

from cloudtea.widgets import base

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

    def add_item(self, widget, last=False):
        if last:
            self._layout.addWidget(widget)
        else:
            lastIndex = self._layout.count()
            if lastIndex:
                self._layout.insertSpacing(0, 10)
                self._layout.insertWidget(1, widget)
            else:
                self._layout.addSpacing(10)
                self._layout.addWidget(widget)
                self._layout.addStretch(1)

    def clean(self):
        for i in reversed(range(self._layout.count())):
            item = self._layout.takeAt(i).widget()
            if item:
                item.setParent(None)

class ListItem(base.TFrame):
    def __init__(self, app, parent=None):
        super(ListItem, self).__init__(parent)
        self._app = app
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

    def add_item(self, item):
        self._layout.addWidget(item)

class Panel(base.TFrame):
    def __init__(self, app, parent=None):
        super(Panel, self).__init__(parent)
        self._app = app

        self._layout = QVBoxLayout(self)
        self.sidebar_panel = ListItem(self._app)
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

class Panel_Container(base.TScrollArea):
    def __init__(self, app, parent=None,width=None):
        super(Panel_Container, self).__init__(parent)
        self._app = app

        self.panel = Panel(self._app)
        self.listitem = self.panel.sidebar_panel
        self._layout = QVBoxLayout(self)
        self.setWidget(self.panel)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setObjectName('c_left_panel_container')
        self.set_theme_style()
        if width:
            self.setMinimumWidth(width)
            self.setMaximumWidth(width)
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


class PayUi(base.TDialog):
    def __init__(self, app, parent=None):
        super(PayUi, self).__init__(parent)
        self._app = app
        self.setObjectName('biling')
        self._box = QHBoxLayout()
        self._layout = QVBoxLayout(self)

        self.top_panel = TopPanel(app, self)
        self.category_panel = Panel_Container(app, self, 160)
        self.inventory_panel = Panel_Container(app, self, 300)
        self.bil_Panel = Panel_Container(app, self)

        self.set_theme_style()
        self.setup_ui()

    def setup_ui(self):
        self.resize(800, 600)
        self._box.setContentsMargins(0, 0, 0, 0)
        self._box.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._box.addWidget(self.category_panel)
        self._box.addWidget(self.inventory_panel)
        self._box.addWidget(self.bil_Panel)
        self._layout.addWidget(self.top_panel)
        self._layout.addLayout(self._box)

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