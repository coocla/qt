#coding:utf-8
import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QTextCodec, Qt

from cloudtea import logger_config, utils
from cloudtea.db import api
from cloudtea.consts import DEFAULT_THEME_NAME
from cloudtea.views import login, ui
from cloudtea.widgets import base, status, pay
from cloudtea.plugins import PluginsManager
from cloudtea.themes import ThemesManager


#QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))

class App(base.TFrame):
    def __init__(self, user=None):
        super(App, self).__init__()
        self.user = user
        
        self.plugins_manager = PluginsManager(self, self.user)
        self.tips_manager = status.TipsManager(self)
        self.theme_manager = ThemesManager(self)
        self.theme_manager.set_theme(DEFAULT_THEME_NAME)
        self.player_pixmap = None

        self.ui = ui.UI(self)
        self.payui = pay.PayUi(self)
        #初始化所有的管理类
        self._init_managers()

        self.resize(1100, 618)
        self.setObjectName('app')
        #QApplication.setWindowIcon(QIcon(APP_ICON))
        self.set_theme_style()
        self.bind_signal()
        self.show_current_desktop()

    def set_theme_style(self):
        theme = self.theme_manager.current_theme 
        style_str = '''
            #{0} {{ 
                background: {1}; 
                color: {2}; 
            }} 
        '''.format(self.objectName(), 
                   theme.background.name(), 
                   theme.foreground.name()) 
        self.setStyleSheet(style_str) 


    def bind_signal(self):
        side_panel = self.ui.side_panel.left_panel.sidebar_panel
        status_panel = self.ui.status_panel

        side_panel.current_side_item.clicked.connect(self.show_current_desktop)
        status_panel.theme_switch_btn.signal_change_theme.connect(
            self.theme_manager.choose)
        status_panel.theme_switch_btn.clicked.connect(
            self.refresh_themes)
        self.ui.refresh_btn.clicked.connect(self.ready_show_data)
        self.ui.current_desktop.cellDoubleClicked.connect(self.ready_show_pay)
        self.payui.metering_dialog.ok_btn.clicked.connect(self.push_shopping_car)

    def _init_managers(self):
        self.plugins_manager.load_plugins()
        self.tips_manager.show_random_tip()

    def message(self, text, error=False):
        self.ui.status_panel.message_label.show_message(text, error)

    def paintEvent(self, event):
        painter = QPainter(self)
        bg_color = utils.darker(self.theme_manager.current_theme.background, a=200)
        if self.player_pixmap is not None:
            pixmap = self.player_pixmap.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, pixmap)
            painter.fillRect(self.rect(), bg_color)

    def refresh_themes(self):
        theme_switch_btn = self.ui.status_panel.theme_switch_btn
        themes = self.theme_manager.list()
        theme_switch_btn.set_themes(themes)

    def show_request_progress(self, progress):
        self.ui.status_panel.network_status_label.show_progress(progress)

    def ready_show_data(self):
        self.ui.current_desktop.set_data(api.list_room())

    def show_current_desktop(self):

        self.message(u'提醒: 已切换至 桌面 菜单')
        self.ui.central_panel.top_panel.clean()  # 重置功能菜单
        self.ready_show_data()
        right_panel = self.ui.central_panel.right_panel
        right_panel.set_widget(self.ui.current_desktop)

        top_panel = self.ui.central_panel.top_panel
        top_panel.add_item(self.ui.refresh_btn)
        top_panel.add_item(self.ui.vip_create_btn)
        top_panel.add_item(self.ui.vip_recharge_btn)

    def ready_show_pay(self, row, column):
        table = self.sender()
        pos = table.lineNum * row + column + 1
        if len(table.data) < pos:
            return
        self.payui.category_panel.listitem.clean()
        # 添加默认的全部分类器
        item = base.TGroupItem(self, u'全部')
        item.set_img_text('>')
        item.set_item_value(0)
        item.clicked.connect(self.inventory_filter_category)
        self.payui.category_panel.listitem.add_item(item)

        for cate in api.list_category():
            item = base.TGroupItem(self, cate.name)
            item.set_img_text('>')
            item.set_item_value(cate.id)
            item.clicked.connect(self.inventory_filter_category)
            self.payui.category_panel.listitem.add_item(item)
        self.fill_inventory(api.list_inventory())
        self.payui.show()

    def fill_inventory(self, data):
        self.payui.inventory_panel.listitem.clean()
        for inventory in data:
            item = base.TCItem(self, inventory)
            item.clicked.connect(self.confirm_shopping_car)
            self.payui.inventory_panel.listitem.add_item(item)

    def inventory_filter_category(self):
        self.payui.inventory_panel.listitem.clean()
        pk = self.sender().item_value
        if pk == 0:
            self.fill_inventory(api.list_inventory())
        else:
            category = api.get_category(pk)
            self.fill_inventory(category.inventory.all())
        

    def confirm_shopping_car(self):
        inventory_id = self.sender().item_value
        self.payui.metering_dialog.set_inventory(inventory_id)
        self.payui.metering_dialog.show()

    def push_shopping_car(self):
        Msg = base.Message('warning', self.payui.metering_dialog)
        number = self.payui.metering_dialog._input.text()
        try:
            number = int(number.strip())
        except:
            Msg.show(u'错误', u'请填写合法的数字')
            return
        inventory = api.get_inventory(self.payui.metering_dialog.item_value)
        if number > inventory.number * inventory.suttle:
            Msg.show(u'错误', u'库存不够了, 剩余: %s, 让老板进货吧!!!' % inventory.number * inventory.suttle)
            return
        self.payui.metering_dialog.hide()

        pre_sale = base.ShopItem(self, inventory, number)
        self.payui.bil_Panel.listitem.add_item(pre_sale)



if __name__ == '__main__':
    logger_config()
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setApplicationName(u'浮云茶舍管理系统')
    login_view = login.LoginWindow()
    login_view.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    if login_view.exec_() == QDialog.Accepted:
        main_app = App(login_view.user)
        main_app.show()
        app.exec_()