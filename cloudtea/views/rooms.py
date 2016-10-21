#coding:utf-8
from PySide import QtCore
from PySide.QtGui import *
from PySide.QtSql import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except:
    _fromUtf8 = lambda s:s



class RoomBtn(QPushButton):
    def __init__(self):
        super(RoomBtn, self).__init__()

    def set_theme_style(self):
        pass


