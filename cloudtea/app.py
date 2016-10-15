#coding:utf-8
import sys
import os
import qdarkstyle
from PySide.QtGui import *
from PySide.QtCore import *

from cloudtea.views import login, main

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_view = login.LoginWindow()
    login_view.setStyleSheet(qdarkstyle.load_stylesheet())
    if login_view.exec_() == QDialog.Accepted:
        widget = main.MainWindow()
        widget.show()
        app.exec_()