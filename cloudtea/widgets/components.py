#coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QColor

from cloudtea.db import api
from cloudtea.utils import darker
from cloudtea.widgets import base



class RoomItem(QTableWidgetItem):
    def __init__(self, app, item):
        super(RoomItem, self).__init__()
        self._app = app
        self.setText(item.name)
        self.room_id = item.id
        self.setup_ui()

    def setup_ui(self):
        self.setTextAlignment(Qt.AlignCenter)
        self.setup_color()

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
        #self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.cellDoubleClicked.connect(self.on_cell_dbclick)

        self.setObjectName('music_table')
        self.set_theme_style()
        self.lineNum=8
        self.data=[]
        self.desktop_width = self._app.width() - 160 - 60
        self.box_size=96
        self.lineNum = self.desktop_width//self.box_size
        print(self.lineNum)

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
        #name_item = RoomItem(self._app, model_data)
        #This is dev data
        name_item = QTableWidgetItem(model_data['name'])
        name_item.setTextAlignment(Qt.AlignCenter)
        if model_index%2:
            name_item.setBackground(QColor(214,114,113))

        row = model_index//self.lineNum
        column = model_index%self.lineNum
        if self.columnCount() != self.lineNum and model_index >= self.lineNum-1:
            self.setColumnCount(self.lineNum)
        self.setRowCount(model_index//self.lineNum+1)
        self.setItem(row, column, name_item)
        self.setColumnWidth(column, self.box_size)
        self.setRowHeight(row, self.box_size)
        if not resize:
            self.data.append(model_data)

    def set_data(self, datas, resize=False):
        self.setRowCount(0)
        for index, data in enumerate(datas):
            self.add_item(index, data, resize=resize)

class RoomTable(base.TTableWidget):
    def __init__(self, app, rows=0, columns=7, parent=None):
        super(RoomTable, self).__init__(rows, columns, parent)
        self._app = app

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  #按行选择
        self._alignment = Qt.AlignLeft | Qt.AlignVCenter
        self.horizontalHeader().setDefaultAlignment(self._alignment)
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)

        self.setObjectName('music_table')
        self.set_theme_style()
        self.data = []

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
        name_item = QTableWidgetItem(model_data.name)

        row = self.rowCount()
        self.setRowCount(row+1)
        self.setItem(row, 1, name_item)
        self.data.append(model_data)

    def set_data(self, datas):
        self.setRowCount(0)
        for data in datas:
            self.add_item(data)

