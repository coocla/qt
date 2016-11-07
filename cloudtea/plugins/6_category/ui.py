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

class CategoryTable(base.TTableWidget):
    def __init__(self, app, rows=0, columns=3, parent=None):
        super(CategoryTable, self).__init__(rows, columns, parent)
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

        self.setHorizontalHeaderLabels(['', u'分类名', u'该类货品数'])
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
        inventory = QTableWidgetItem('%s' % model_data.inventory.count())

        row = self.rowCount()
        self.setRowCount(row+1)
        self.setItem(row, 1, name)
        self.setItem(row, 2, inventory)
        self.data.append(model_data)

    def set_data(self, datas):
        self.setRowCount(0)
        self.data = []
        for data in datas:
            self.add_item(data)


class UI(object):
    def __init__(self, app):
        self._app = app
        self.category_item = base.TGroupItem(self._app, u'货品分类')
        self.category_item.set_img_text('>')
        self.search_box = base.SearchBox(self._app)
        self.delcategory_btn = base.TLButton(self._app, u'删除分类')
        self.newcategory_btn = base.TLButton(self._app, u'新增分类')
        self.refresh_btn = base.TLButton(self._app, u'刷新')
        self.newcategory_dialog = CategoryDialog(self._app)
        self.setup_ui()

    def setup_ui(self):
        top_panel = self._app.ui.central_panel.top_panel
        side_panel = self._app.ui.side_panel.left_panel
        side_panel.sidebar_panel.add_item(self.category_item)
        self.desktop = CategoryTable(self._app)