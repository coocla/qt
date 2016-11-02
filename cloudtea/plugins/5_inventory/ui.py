#coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QVBoxLayout

from cloudtea.utils import darker
from cloudtea.widgets import base


class InventoryDialog(base.TDialog):
    def __init__(self, app, parent=None):
        super(InventoryDialog, self).__init__(parent)
        self._app = app

class InventoryTable(base.TTableWidget):
    def __init__(self, app, rows=0, columns=8, parent=None):
        super(InventoryTable, self).__init__(rows, columns, parent)
        self._app = app

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  #按行选择
        self._alignment = Qt.AlignLeft | Qt.AlignVCenter
        self.horizontalHeader().setDefaultAlignment(self._alignment)
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)

        self.setObjectName('music_table')
        self.set_theme_style()
        self.data = []

        self.setColumnWidth(0, 28)
        self.setColumnWidth(1, 170)
        self.setColumnWidth(2, 170)
        self.setColumnWidth(5, 170)

        self.setHorizontalHeaderLabels(['', u'品名', u'数量', u'规格', u'价格', u'所属类别', u'净重', u'计量方式'])
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.cellDoubleClicked.connect(self.on_cell_dbclick)

    def on_cell_dbclick(self, row, column):
        print('Double here %s,%s' % (row, column))

    def set_theme_style(self): 
        theme = self._app.theme_manager.current_theme 
        style_str = ''' 
            QHeaderView {{ 
                color: {1}; 
                background: transparent; 
                font-size: 14px; 
            }} 
            QHeaderView::section:horizontal {{ 
                height: 24px; 
                background: transparent; 
                border-top: 1px; 
                border-right: 1px; 
                border-bottom: 1px; 
                border-color: {5}; 
                color: {5}; 
                border-style: solid; 
                padding-left: 5px; 
            }} 
 
            QTableView QTableCornerButton::section {{ 
                background: transparent; 
                border: 0px; 
                border-bottom: 1px solid {1}; 
            }} 
            #{0} {{ 
                border: 0px; 
                background: transparent; 
                alternate-background-color: {3}; 
                color: {1}; 
            }} 
            #{0}::item {{ 
                color: {1}; 
                outline: none; 
            }} 
            #{0}::item:focus {{ 
                background: transparent; 
                outline: none; 
            }} 
            #{0}::item:selected {{ 
                background: {4}; 
            }} 
        '''.format(self.objectName(), 
                   theme.foreground.name(), 
                   theme.color6.name(), 
                   darker(theme.color0, a=30).name(QColor.HexArgb), 
                   theme.color0.name(), 
                   theme.color7_light.name()) 
        self.setStyleSheet(style_str)

    def add_item(self, model_data):
        name = QTableWidgetItem(model_data.name)
        vip_id = QTableWidgetItem('%s' % model_data.vip_id)
        amount = QTableWidgetItem('%s' % model_data.amount)
        phone = QTableWidgetItem('%s' % model_data.phone)
        created_at = QTableWidgetItem(str(model_data.created_at))

        row = self.rowCount()
        self.setRowCount(row+1)
        self.setItem(row, 1, name)
        self.setItem(row, 2, vip_id)
        self.setItem(row, 3, phone)
        self.setItem(row, 4, amount)
        self.setItem(row, 5, created_at)
        self.data.append(model_data)

    def set_data(self, datas):
        self.setRowCount(0)
        for data in datas:
            self.add_item(data)


class UI(object):
    def __init__(self, app):
        self._app = app
        self.inventory_item = base.TGroupItem(self._app, u'库存管理')
        self.inventory_item.set_img_text('>')
        self.search_box = base.SearchBox(self._app)
        self.delinventory_btn = base.TLButton(self._app, u'删除货品')
        self.newinventory_btn = base.TLButton(self._app, u'新增会员')
        self.refresh_btn = base.TLButton(self._app, u'刷新')
        self.setup_ui()

    def setup_ui(self):
        top_panel = self._app.ui.central_panel.top_panel
        side_panel = self._app.ui.side_panel.left_panel
        side_panel.sidebar_panel.add_item(self.inventory_item)
        self.desktop = InventoryTable(self._app)