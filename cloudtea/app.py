#coding:utf-8
import sys
import qdarkstyle
from PySide.QtGui import QApplication, QDialog, QIcon
from PySide.QtCore import QTextCodec

from cloudtea import logger_config
from cloudtea.consts import DEFAULT_THEME_NAME
from cloudtea.views import login, ui
from cloudtea.widgets import base
from cloudtea.plugins import PluginsManager
from cloudtea.themes import ThemesManager


QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))

class App(base.TFrame):
    def __init__(self, user=None):
        super(App, self).__init__()
        self.user = user

        self.plugins_manager = PluginsManager(self, self.user)
        self.theme_manager = ThemesManager(self)
        self.theme_manager.set_theme(DEFAULT_THEME_NAME)

        self.ui = ui.UI(self)
        #初始化所有的管理类
        self._init_managers()

        self.resize(1000, 618)
        self.setObjectName('app')
        #QApplication.setWindowIcon(QIcon(APP_ICON))
        self.set_theme_style()
        self.bind_signal()

    def set_theme_style(self):
        pass

    def bind_signal(self):
        pass

    def _init_managers(self):
        print 'Start load plugins'
        self.plugins_manager.load_plugins()

if __name__ == '__main__':
    logger_config()
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setApplicationName(u'浮云茶舍管理系统')
    login_view = login.LoginWindow()
    login_view.setStyleSheet(qdarkstyle.load_stylesheet())
    if login_view.exec_() == QDialog.Accepted:
        main_app = App(login_view.user)
        main_app.show()
        app.exec_()