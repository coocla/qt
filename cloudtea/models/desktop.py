#coding:utf-8
from PySide.QtSql import *
from PySide.QtCore import *


class RoomModel(QSqlTableModel):
	def __init__(self):
		super(RoomModel, self).__init__()

	def data(self, index, role=Qt.DisplayRole):
		return 'admin'

	def headerData(self, section, orientation, role=Qt.DisplayRole):
		head = [u'ID', u'姓名', u'性别', u'年龄', u'联系电话', u'添加日期']
		return head[section]


def roomModel():
	model = QSqlTableModel()
	model.setTable('users')
	if (model.select()):
		model.removeColumn(0)
		model.setHeaderData(1, Qt.Horizontal, u"姓名")
		model.setHeaderData(2, Qt.Horizontal, u"性别")
		model.setHeaderData(3, Qt.Horizontal, u"年龄")
		model.setHeaderData(4, Qt.Horizontal, u"添加日期")
	#print dir(model)
	#print model.headerData(1, Qt.Horizontal)
	return model