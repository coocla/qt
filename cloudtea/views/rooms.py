#coding:utf-8
from PySide import QtCore
from PySide.QtGui import *
from PySide.QtSql import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except:
    _fromUtf8 = lambda s:s

class RoomView(QWidget):
    def __init__(self,):
        super(RoomView, self).__init__()
        self.box = QGridLayout()
        self.initUI()

    def initUI(self):
        model = QSqlQueryModel()
        model.setQuery('select * from rooms')
        for index in range(0, model.rowCount()):
            name = model.record(index).value('name')
            inused = model.record(index).value('inused')



