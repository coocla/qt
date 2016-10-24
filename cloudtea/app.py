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
from cloudtea.widgets import base, status
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
        #初始化所有的管理类
        self._init_managers()

        self.resize(1000, 618)
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

    def show_current_desktop(self):
        self.ui.central_panel.top_panel.clean()  # 重置功能菜单
        datas = api.list_room()
        # This is dev data
        datas=[
            {"name":u"风花雪月"}, 
            {"name":u"小桥流水"},
            {"name":u"枯藤老树"},
            {"name":u"葵花宝典"},
            {"name":u"九阳真经"},
            {"name":u"六脉神剑"},
            {"name":u"凌波微步"},
            {"name":u"隔山打牛"},
            {"name":u"九阴真经"},
            {"name":u"如来神掌"},
            {"name":u"六脉神剑"},
            {"name":u"移花接木"},
            {"name":u"神龙摆尾"},
            {"name":u"二龙戏珠"},
            {"name":u"打狗棒法"}
        ]
        self.ui.current_desktop.set_data(datas)
        right_panel = self.ui.central_panel.right_panel
        right_panel.set_widget(self.ui.current_desktop)

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