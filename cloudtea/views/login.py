#coding:utf-8
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from cloudtea.db import api, utils
from cloudtea.widgets import base
from cloudtea.views import widgets

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

def _fromUtf8(s):
	return s

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.user = None
        self.setupUi()
        self.setWindowTitle(u'浮云茶舍')
        
    def setupUi(self):
        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(160, 120, 531, 321))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(130, 80, 61, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(130, 130, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.username = QLineEdit(self.groupBox)
        self.username.setGeometry(QtCore.QRect(200, 70, 221, 31))
        self.username.setObjectName(_fromUtf8("username"))
        self.password = QLineEdit(self.groupBox)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(QtCore.QRect(200, 120, 221, 31))
        self.password.setObjectName(_fromUtf8("password"))
        self.login_btn = QPushButton(self.groupBox)
        self.login_btn.setGeometry(QtCore.QRect(160, 220, 75, 23))
        self.login_btn.setObjectName(_fromUtf8("login_btn"))
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 220, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi()
        self.pushButton_2.clicked.connect(self.close)
        # QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.close)
        self.login_btn.clicked.connect(self.login)

    def login(self):
        username = self.username.text().encode('utf-8')
        password = self.password.text().encode('utf-8')
        self.user = api.get_user(username)
        if self.user and utils.check_password(password, self.user.password):
            self.accept()
        else:
            box=base.Message('warning', self)
            box.show(u'错误', u'账户或密码错误!')
            
    def retranslateUi(self):
        self.groupBox.setTitle(_translate("Dialog", "登录系统", None))
        self.label.setText(_translate("Dialog", "登录账户：", None))
        self.label_2.setText(_translate("Dialog", "登录密码：", None))
        self.login_btn.setText(_translate("Dialog", "登录", None))
        self.pushButton_2.setText(_translate("Dialog", "退出", None))