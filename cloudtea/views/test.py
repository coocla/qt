#coding:utf-8
import sys
import os
import qdarkstyle
from PySide.QtGui import *
from PySide.QtCore import *

from cloudtea.views import login

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(qdarkstyle.load_stylesheet())
	login_view = login.LoginWindow()
	if login_view.exec_() == QDialog.Accepted:
		widget = QWidget()
		widget.show()
		app.exec_()