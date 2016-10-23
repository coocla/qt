PyQt5#coding:utf-8
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtSql import *

from cloudtea.libs import utils
from cloudtea.views import widgets


class UserDelegate(QStyledItemDelegate):
    def __init__(self):
        super(UserDelegate, self).__init__()

    def paint(self, painter, option, index):
        model = index.model()
        sex_index = model.fieldIndex('sex')
        if index.column() == sex_index:
            if model.data(index, QtCore.Qt.DisplayRole):
                painter.drawText(option.rect, QtCore.Qt.AlignCenter, u'女')
            else:
                painter.drawText(option.rect, QtCore.Qt.AlignCenter, u'男')
        else:
            super(UserDelegate, self).paint(painter, option, index)


class NewUserDialog(QDialog):
    """docstring for NewUserDialog"""
    def __init__(self):
        super(NewUserDialog, self).__init__()
        self.setWindowTitle(u'新增用户')
        self.box = QGridLayout()
        self.initWidget()
        self.setGeometry(QtCore.QRect(160, 120, 500, 150))

    def initWidget(self):
        fields = [
            {"k":"name", "v":u"姓名:"},
            {"k":"username","v":u"账户:"},
            {"k":"password", "v":u"密码:"},
            {"k":"confirm_password", "v":u"确认密码:"},
            {"k":"phone","v":u"联系方式:"},
        ]
        name_label = QLabel(u"姓名")
        self.name_input = QLineEdit()
        self.box.addWidget(name_label, 0, 0)
        self.box.addWidget(self.name_input, 0,1)
        username_label = QLabel(u"账户")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(u'使用英文或数字的组合')
        self.box.addWidget(username_label, 1, 0)
        self.box.addWidget(self.username_input, 1, 1)
        password_label = QLabel(u'密码')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.box.addWidget(password_label, 2, 0)
        self.box.addWidget(self.password_input, 2, 1)
        confirm_password_label = QLabel(u'确认密码')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.box.addWidget(confirm_password_label, 3, 0)
        self.box.addWidget(self.confirm_password_input, 3, 1)
        phone_label = QLabel(u'联系方式')
        self.phone_input = QLineEdit()
        self.box.addWidget(phone_label, 4, 0)
        self.box.addWidget(self.phone_input, 4, 1)


        ext_index = len(fields)
        agelabel = QLabel(u'年龄')
        self.agebox = QSpinBox()
        self.agebox.setRange(18,80)
        self.box.addWidget(agelabel, *(ext_index, 0))
        self.box.addWidget(self.agebox, *(ext_index, 1))

        sexlabel = QLabel(u'性别')
        self.sexbox = QComboBox()
        self.sexbox.addItems([u'男', u'女'])
        self.box.addWidget(sexlabel, *(ext_index+1, 0))
        self.box.addWidget(self.sexbox, *(ext_index+1, 1))

        create_user_btn = QPushButton(u'确认')

        self.vbox = QVBoxLayout()

        self.vbox.addLayout(self.box)
        self.vbox.addWidget(create_user_btn)

        self.setLayout(self.vbox)

        create_user_btn.clicked.connect(self.submit_create)

    def submit_create(self):
        model = QSqlTableModel()
        if unicode(self.password_input.text()) != unicode(self.confirm_password_input.text()):
            QMessageBox.information(self, u'提示', u'两次输入的密码不一致')
            return
        model.setFilter('name="%s" or username="%s"' % (unicode(self.name_input.text()), unicode(self.username_input.text())))
        if model.select() and model.rowCount() >= 1:
            QMessageBox.information(self, u'提示', u'姓名或账户已经被占用!')
            return
        model.setTable('users')
        model.insertRows(0, 1)
        model.setData(model.index(0,  model.fieldIndex('name')), unicode(self.name_input.text()))
        model.setData(model.index(0,  model.fieldIndex('username')), unicode(self.username_input.text()))
        model.setData(model.index(0,  model.fieldIndex('password')), utils.make_password(self.password_input.text()))
        model.setData(model.index(0,  model.fieldIndex('phone')), unicode(self.phone_input.text()))
        model.setData(model.index(0,  model.fieldIndex('age')), self.agebox.value())
        model.setData(model.index(0,  model.fieldIndex('sex')), self.sexbox.currentIndex())
        model.setData(model.index(0,  model.fieldIndex('role')), 1)
        model.setData(model.index(0,  model.fieldIndex('created_at')), unicode(utils.now()))
        model.submitAll()
        self.close()
