#coding:utf-8
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QWidgetItem
from PyQt5.QtCore import Qt

from cloudtea.widgets import base, components

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
        self._layout.addStretch(1)

    def add_item(self, widget, last=False):
        self._layout.addSpacing(10)
        self._layout.addWidget(widget)

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
        # self._layout.addSpacing(8)

    def add_item(self, item):
        self._layout.addWidget(item)

    def clean(self):
        for i in reversed(range(self._layout.count())):
            item = self._layout.takeAt(i).widget()
            if item:
                item.setParent(None)

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

    def resize(self, width):
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

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


class Metering(base.TDialog):
    def __init__(self, app, parent=None):
        super(Metering, self).__init__(parent)
        self._app = app
        self._layout = QVBoxLayout()
        self._box = QHBoxLayout()
        self._vbox = QHBoxLayout()
        self.item_value = None
        self._tip_label = base.TLabel(u'请输入数量', self)
        self._input = components.Input(self._app)
        self.ok_btn = base.TLButton(self._app, u'提交', size=12)
        self.setup_ui()
        self._input.returnPressed.connect(self.ok_btn.clicked)


    def setup_ui(self):
        self.resize(250, 100)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._box.addStretch(1)
        self._box.addSpacing(40)
        self._box.addWidget(self._tip_label)
        self._box.addSpacing(10)
        self._box.addWidget(self._input)
        self._box.addSpacing(40)
        self._vbox.addStretch(1)
        self._vbox.addWidget(self.ok_btn)
        self._vbox.addSpacing(30)

        self._layout.addSpacing(30)
        self._layout.addLayout(self._box)
        self._layout.addLayout(self._vbox)
        self.setLayout(self._layout)

    def set_inventory(self, inventory_id):
        self.item_value = inventory_id

    def reset(self):
        self._input.setText('')

    def hideEvent(self, event):
        self.reset()

    def closeEvent(self, event):
        self.reset()

class PayUi(base.TDialog):
    def __init__(self, app, parent=None):
        super(PayUi, self).__init__(parent)
        self._app = app
        self.setObjectName('biling')
        self._box = QHBoxLayout()
        self._layout = QVBoxLayout(self)

        self.biling_btn = base.TLButton(self._app, u'结账', size=20)
        self.overview_label = base.TLabel(self._app)

        self.top_panel = TopPanel(app, self)
        self.category_panel = Panel_Container(app, self, 160)
        self.inventory_panel = Panel_Container(app, self, 400)
        self.bil_Panel = Panel_Container(app, self)
        self.metering_dialog = Metering(self._app)

        self.set_theme_style()
        self.setup_ui()

    def resizeEvent(self, event):
        width = self.width() - 210
        self.inventory_panel.resize(width//2)

    def setup_ui(self):
        self.resize(1050, 600)
        self._box.setContentsMargins(0, 0, 0, 0)
        self._box.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._box.addWidget(self.category_panel)
        self._box.addWidget(self.inventory_panel)
        self._box.addWidget(self.bil_Panel)
        self._layout.addWidget(self.top_panel)
        self._layout.addLayout(self._box)
        self.top_panel.add_item(self.biling_btn, last=True)
        self.top_panel.add_item(self.overview_label)

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