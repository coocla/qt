#coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QColor, QFont, QPalette

from cloudtea.db import api
from cloudtea.utils import darker
from cloudtea.widgets import base


class ModalHeader(base.TFrame):
    def __init__(self, app, parent=None):
        super(ModalHeader, self).__init__(parent)
        self._app = app
        self.setObjectName('m_head')
        self.name_item = base.TLabel(self)
        self.name_item.setObjectName('m_header')
        self._layout = QHBoxLayout(self)

        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = ''' 
            #{0} {{ 
                background: transparent;
                border: 0px;
                border-bottom: 3px inset {1};
            }}
            #{2} {{
                font-size: 22px;
                color: {3}
            }}
         '''.format(self.objectName(), 
                theme.color0_light.name(),
                self.name_item.objectName(),
                theme.color7_light.name())
        self.setStyleSheet(style_str) 

    def setup_ui(self):
        self.setFixedHeight(50)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.name_item)
        self._layout.addStretch(1)

    def set_header(self, text):
        self.name_item.setText(text)

class ModalBody(base.TFrame):
    def __init__(self, app, parent=None):
        super(ModalBody, self).__init__(parent)
        self._app = app
        self.setObjectName('m_body')
        self._layout = QHBoxLayout(self)

        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
                border: 0px;
                border-bottom: 3px inset {1};
            }}
        '''.format(self.objectName(),
                   theme.color0_light.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

    def add_item(self, widget=None):
        if widget:
            try:
                self._layout.addWidget(widget)
            except:
                self._layout.addLayout(widget)
        else:
            self._layout.addStretch(1)

class ModalFooter(base.TFrame):
    def __init__(self, app, parent=None):
        super(ModalFooter, self).__init__(parent)
        self._app = app
        self.setObjectName('m_foot')
        self._layout = QHBoxLayout(self)

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
        self.setFixedHeight(40)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addStretch(1)

    def add_item(self, widget):
        self._layout.addWidget(widget)
        self._layout.addSpacing(20)


class RoomItem(QTableWidgetItem):
    def __init__(self, app, item):
        super(RoomItem, self).__init__()
        self._app = app
        self.setText(item.name)
        self.room_id = item.id
        self.setup_ui(item)

    def setup_ui(self, item):
        self.setTextAlignment(Qt.AlignCenter)
        self.setup_color(item)

    def setup_color(self, item):
        if item.inused:
            self.setBackground(QColor(214,114,113))
        

class RoomDesktop(base.TTableWidget):
    def __init__(self, app, rows=0, columns=7, parent=None):
        super(RoomDesktop, self).__init__(rows, columns, parent)
        self._app = app
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._alignment = Qt.AlignHCenter | Qt.AlignVCenter
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setAlternatingRowColors(True)
        self.cellDoubleClicked.connect(self.on_cell_dbclick)

        self.setObjectName('music_table')
        self.set_theme_style()
        self.lineNum=8
        self.data=[]
        self.desktop_width = self._app.width() - 160 - 60
        self.box_size=96
        self.lineNum = self.desktop_width//self.box_size

    def resizeEvent(self, event):
        self.desktop_width = self._app.width() - 160 - 60
        self.lineNum = self.desktop_width//self.box_size
        self.resizeTable()

    def resizeTable(self):
        self.set_data(self.data, resize=True)

    def set_theme_style(self): 
        theme = self._app.theme_manager.current_theme 
        style_str = ''' 
            QHeaderView {{ 
                color: {1}; 
                background: transparent; 
                font-size: 14px; 
            }} 
            QHeaderView::section:horizontal {{ 
                height: 24px; 
                background: transparent; 
                border-top: 1px; 
                border-right: 1px; 
                border-bottom: 1px; 
                border-color: {5}; 
                color: {5}; 
                border-style: solid; 
                padding-left: 5px; 
            }} 
 
            QTableView QTableCornerButton::section {{ 
                background: transparent; 
                border: 0px; 
                border-bottom: 1px solid {1}; 
            }} 
            #{0} {{ 
                border: 0px; 
                background: transparent; 
                alternate-background-color: {3}; 
                color: {1}; 
            }} 
            #{0}::item {{ 
                color: {1}; 
                outline: none; 
            }} 
            #{0}::item:focus {{ 
                background: transparent; 
                outline: none; 
            }} 
            #{0}::item:selected {{ 
                background: {4}; 
            }}
        '''.format(self.objectName(), 
                   theme.foreground.name(), 
                   theme.color6.name(), 
                   darker(theme.color0, a=30).name(QColor.HexArgb), 
                   theme.color0.name(), 
                   theme.color7_light.name())
        self.setStyleSheet(style_str)

    def on_cell_dbclick(self, row, column):
        print('Double here %s,%s' % (row, column))

    def add_item(self, model_index, model_data, resize=False):
        name_item = RoomItem(self._app, model_data)
        row = model_index//self.lineNum
        column = model_index%self.lineNum
        if self.columnCount() != self.lineNum and model_index >= self.lineNum-1:
            self.setColumnCount(self.lineNum)
        else:
            self.setColumnCount(model_index+1)
        self.setRowCount(model_index//self.lineNum+1)
        self.setItem(row, column, name_item)
        self.setColumnWidth(column, self.box_size)
        self.setRowHeight(row, self.box_size)
        if not resize:
            self.data.append(model_data)

    def set_data(self, datas, resize=False):
        self.setRowCount(0)
        if not resize:
            self.data = []
        for index, data in enumerate(datas):
            self.add_item(index, data, resize=resize)

class RoomTable(base.TTableWidget):
    def __init__(self, app, rows=0, columns=7, parent=None):
        super(RoomTable, self).__init__(rows, columns, parent)
        self._app = app

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.setSelectionMode(QAbstractItemView.ExtendedSelection) #可多选
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  #按行选择
        self._alignment = Qt.AlignLeft | Qt.AlignVCenter
        self.horizontalHeader().setDefaultAlignment(self._alignment)
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)

        self.setObjectName('music_table')
        self.set_theme_style()
        self.data = []

        self.setColumnWidth(0, 28)
        self.setColumnWidth(6, 170)

        self.setHorizontalHeaderLabels(['', u'房间名', u'使用中', u'会员房费', u'普通房费', u'客人容量', u'添加时间'])
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.cellDoubleClicked.connect(self.on_cell_dbclick)

    def on_cell_dbclick(self, row, column):
        print('Double here %s,%s' % (row, column))

    def set_theme_style(self): 
        theme = self._app.theme_manager.current_theme 
        style_str = ''' 
            QHeaderView {{ 
                color: {1}; 
                background: transparent; 
                font-size: 14px; 
            }} 
            QHeaderView::section:horizontal {{ 
                height: 24px; 
                background: transparent; 
                border-top: 1px; 
                border-right: 1px; 
                border-bottom: 1px; 
                border-color: {5}; 
                color: {5}; 
                border-style: solid; 
                padding-left: 5px; 
            }} 
 
            QTableView QTableCornerButton::section {{ 
                background: transparent; 
                border: 0px; 
                border-bottom: 1px solid {1}; 
            }} 
            #{0} {{ 
                border: 0px; 
                background: transparent; 
                alternate-background-color: {3}; 
                color: {1}; 
            }} 
            #{0}::item {{ 
                color: {1}; 
                outline: none; 
            }} 
            #{0}::item:focus {{ 
                background: transparent; 
                outline: none; 
            }} 
            #{0}::item:selected {{ 
                background: {4}; 
            }} 
        '''.format(self.objectName(), 
                   theme.foreground.name(), 
                   theme.color6.name(), 
                   darker(theme.color0, a=30).name(QColor.HexArgb), 
                   theme.color0.name(), 
                   theme.color7_light.name()) 
        self.setStyleSheet(style_str)

    def add_item(self, model_data):
        name = QTableWidgetItem(model_data.name)
        inuse = base.TagCellWidget(self._app, model_data.inused)
        vp = QTableWidgetItem('%s' % model_data.vip_price)
        cp = QTableWidgetItem('%s' % model_data.common_price)
        capacity = QTableWidgetItem('%s' % model_data.capacity)
        created_at = QTableWidgetItem(str(model_data.created_at))

        row = self.rowCount()
        self.setRowCount(row+1)
        self.setItem(row, 1, name)
        self.setCellWidget(row, 2, inuse)
        self.setItem(row, 3, vp)
        self.setItem(row, 4, cp)
        self.setItem(row, 5, capacity)
        self.setItem(row, 6, created_at)
        self.data.append(model_data)

    def set_data(self, datas):
        self.setRowCount(0)
        for data in datas:
            self.add_item(data)

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