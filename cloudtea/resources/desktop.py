#coding:utf-8
from PySide.QtSql import *
from PySide.QtCore import *


def RoomModel(mapped, hidens=()):
    model = QSqlTableModel()
    model.setTable('users')
    if (model.select()):
        for hiden in hidens:
            model.removeColumn(model.fieldIndex(hiden))
        for field in mapped:
            model.setHeaderData(model.fieldIndex(field['name']), Qt.Horizontal, field['display'])
    return model