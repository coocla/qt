#coding:utf-8
from PySide import QtCore
from PySide.QtGui import *

from cloudtea.views import widgets

class NewUserDialog(QDialog):
    """docstring for NewUserDialog"""
    def __init__(self):
        super(NewUserDialog, self).__init__()
        self.setWindowTitle(u'新增用户')