#coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QVBoxLayout

from cloudtea.utils import darker
from cloudtea.widgets import base, components


class CategoryDialog(base.TDialog):
    def __init__(self, app, parent=None):
        super(CategoryDialog, self).__init__(parent)
        self._app = app
        self.setObjectName('modal')
        self._layout = QVBoxLayout(self)
        self.box = QVBoxLayout()

        self.name = components.Input(self, u'分类名')
        self.ok_btn = base.TLButton(self._app, u'提交', size=19)

        self.head = components.ModalHeader(self._app, self)
        self.body = components.ModalBody(self._app, self)
        self.foot = components.ModalFooter(self._app, self)
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme 
        style_str = '''
            #{0} {{ 
                background: {1}; 
                color: {2}; 
            }} 
        '''.format(self.objectName(), 
                   theme.background.name(), 
                   theme.foreground.name()) 
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self.resize(350, 250)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.head)
        self._layout.addWidget(self.body)
        self._layout.addWidget(self.foot)
        
        self.box.setContentsMargins(0,0,0,0)
        self.box.setSpacing(0)
        self.box.addSpacing(10)
        self.box.addWidget(self.name)
        self.box.addSpacing(10)
        self.box.addStretch(1)

        self.head.set_header(u'添加分类')
        self.foot.add_item(self.ok_btn)
        self.body.add_item()
        self.body.add_item(self.box)
        self.body.add_item()

    def reset(self):
        self.name.setText('')

    def hideEvent(self, event):
        self.reset()

    def closeEvent(self, event):
        self.reset()


class InventoryDialog(base.TDialog):
    def __init__(self, app, parent=None):
        super(InventoryDialog, self).__init__(parent)
        self._app = app
        self.setObjectName('modal')
        self._layout = QVBoxLayout(self)
        self.box = QVBoxLayout()

        self.name = components.Input(self, u'商品名')
        self.specifications = components.Input(self, u'规格')
        self.category = components.Select(self)

        self.number = base.TSpinBox(self)
        self.number.setMinimum(1)
        self.number.setSuffix(u'     入库数量')
        self.meter = components.Select(self)
        self.meter.insertItem(0,'--- 包装方式 ---')
        self.meter.addItem(u'散装')
        self.meter.addItem(u'袋/瓶装')
        self.price = components.Input(self, u'售价, 单位: 元')
        self.suttle = components.Input(self, u'可分几次使用, 例如: 10袋/盒,每次最少用1袋,即可分10次使用')

        self.ok_btn = base.TLButton(self._app, u'提交', size=19)

        self.head = components.ModalHeader(self._app, self)
        self.body = components.ModalBody(self._app, self)
        self.foot = components.ModalFooter(self._app, self)
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{ 
                background: {1}; 
                color: {2}; 
            }} 
        '''.format(self.objectName(), 
                   theme.background.name(), 
                   theme.foreground.name()) 
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self.resize(800, 500)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self.head)
        self._layout.addWidget(self.body)
        self._layout.addWidget(self.foot)
        
        self.box.setContentsMargins(0,0,0,0)
        self.box.setSpacing(0)
        self.box.addSpacing(10)
        self.box.addWidget(self.name)
        self.box.addSpacing(10)
        self.box.addWidget(self.specifications)
        self.box.addSpacing(10)
        self.box.addWidget(self.category)
        self.box.addSpacing(10)
        self.box.addWidget(self.number)
        self.box.addSpacing(10)
        self.box.addWidget(self.meter)
        self.box.addSpacing(10)
        self.box.addWidget(self.price)
        self.box.addSpacing(10)
        self.box.addWidget(self.suttle)
        self.box.addStretch(1)

        self.head.set_header(u'添加库存')
        self.foot.add_item(self.ok_btn)
        self.body.add_item()
        self.body.add_item(self.box)
        self.body.add_item()

    def reset(self):
        self.name.setText('')
        self.specifications.setText('')
        self.price.setText('')
        self.suttle.setText('')
        self.category.clear()

    def hideEvent(self, event):
        self.reset()

    def closeEvent(self, event):
        self.reset()

class InventoryTable(base.TTableWidget):
    def __init__(self, app, rows=0, columns=7, parent=None):
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

        self.setHorizontalHeaderLabels(['', u'品名', u'库存', u'价格', u'规格', u'所属类别', u'单品最多消费次数'])
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
        number = QTableWidgetItem('%s' % model_data.number)
        specifications = QTableWidgetItem('%s' % model_data.specifications)
        price = QTableWidgetItem(u'%s 元' % model_data.price)
        category = QTableWidgetItem('%s' % model_data.category.name)
        suttle = QTableWidgetItem('%s' % (model_data.suttle))

        row = self.rowCount()
        self.setRowCount(row+1)
        self.setItem(row, 1, name)
        self.setItem(row, 2, number)
        self.setItem(row, 3, price)
        self.setItem(row, 4, specifications)
        self.setItem(row, 5, category)
        self.setItem(row, 6, suttle)
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
        self.newinventory_btn = base.TLButton(self._app, u'新增货品')
        self.refresh_btn = base.TLButton(self._app, u'刷新')
        self.newinventory_dialog = InventoryDialog(self._app)
        self.newcategory_dialog = CategoryDialog(self._app)
        self.setup_ui()

    def setup_ui(self):
        top_panel = self._app.ui.central_panel.top_panel
        side_panel = self._app.ui.side_panel.left_panel
        side_panel.sidebar_panel.add_item(self.inventory_item)
        self.desktop = InventoryTable(self._app)