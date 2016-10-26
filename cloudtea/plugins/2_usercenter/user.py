#coding:utf-8
from .ui import UI
from cloudtea.widgets import base


class User(base.TObject):
    def __init__(self, app):
        super(User, self).__init__(parent=app)
        self._app = app
        self.ui = UI(self._app)