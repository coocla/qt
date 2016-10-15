#coding:utf-8
from PySide.QtGui import *

class BaseWidget(QWidget):
    def __init__(self):
        super(BaseWidget,self).__init__()
        self.move_center()

    def move_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
