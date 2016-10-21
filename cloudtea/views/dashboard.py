#coding:utf-8
from PySide.QtGui import QHBoxLayout

from cloudtea.db import api
from cloudtea.widgets import base


class DeskTop(base.TFrame):
    def __init__(self, app, parent=None):
        super(DeskTop, self).__init__(parent)
        self._app = app

        self._layout = QHBoxLayout(self)

        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        pass

    def setup_ui(self):
        pass

    