#coding:utf-8
from PySide import QtSql, QtGui
from cloudtea import setting as opt

_MARK = None

def db_engine():
	global _MARK
	if _MARK is None:
		db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
		db.setHostName(opt.db_host)
		db.setDatabaseName(opt.db_name)
		db.setUserName(opt.db_user)
		db.setPassword(opt.db_password)
		db.setPort(opt.db_port)
		if not db.open():
			QtGui.QMessageBox.critical(None, u'错误', u'数据库连接失败, (%s)' % db.lastError().text(), QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)
			import sys
			sys.exit(999)
		_MARK = QtSql.QSqlQuery()
	return _MARK