#coding:utf-8
from .ui import UI
from cloudtea.widgets import base


class WeChat(base.TObject):
    def __init__(self, app, user):
        super(WeChat, self).__init__(parent=app)
        self._app = app
        self.ui = UI(self._app)