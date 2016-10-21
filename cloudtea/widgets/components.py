#coding:utf-8
from PySide.QtCore import Qt, Signal
from PySide.QtGui import QAbstractItemView, QHeaderView, QTableWidgetItem, QHBoxLayout


from cloudtea.widgets import base


class RoomTable(base.TTableWidget):
    def __init__(self, app, rows=0, columns=7, parent=None):
        super(RoomTable, self).__init__(rows, columns, parent)
        self._app = app

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._alignment = Qt.AlignLeft | Qt.AlignVCenter
        self.horizontalHeader().setDefaultAlignment(self._alignment)
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)

        self.setObjectName('room_table')
        self.set_theme_style()
        self.setHorizontalHeaderLabels(['', u'房间名', u'使用中', u'VIP房费', u'普通房费', u'客人容量', u'添加时间'])
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.cellDoubleClicked.connect(self.on_cell_dbclick)

    def on_cell_dbclick(self, row, column):
        print row, column
        print 'Double Clicked'