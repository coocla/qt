#coding:utf-8
from PySide import QtCore
from PySide.QtGui import *

from cloudtea.db import api
from cloudtea.libs import utils
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
        self.password.setGeometry(QtCore.QRect(200, 120, 221, 31))
        self.password.setObjectName(_fromUtf8("password"))
        self.login_btn = QPushButton(self.groupBox)
        self.login_btn.setGeometry(QtCore.QRect(160, 220, 75, 23))
        self.login_btn.setObjectName(_fromUtf8("login_btn"))
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 220, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi()
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.close)
        self.login_btn.clicked.connect(self.login)

    def login(self):
        username = unicode(self.username.text())
        password = unicode(self.password.text())
        self.user = api.get_user(username)
        if 1:
        #if self.user and utils.check_password(self.user.password, password):
            self.accept()
        else:
            showMsg()
            
    def retranslateUi(self):
        self.groupBox.setTitle(_translate("Dialog", "登录系统", None))
        self.label.setText(_translate("Dialog", "登录账户：", None))
        self.label_2.setText(_translate("Dialog", "登录密码：", None))
        self.login_btn.setText(_translate("Dialog", "登录", None))
        self.pushButton_2.setText(_translate("Dialog", "退出", None))

class showMsg(widgets.BaseWidget):
    def __init__(self):
        super(Exp, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(200, 300, 400, 400)
        self.setWindowTitle(u'错误')
        QMessageBox.warning(self, u'错误', u'账户或密码错误!', QMessageBox.Yes, QMessageBox.Yes)
