#coding:utf-8
from .ui import UI
from cloudtea.widgets import base


class VIP(base.TObject):
    def __init__(self, app, user):
        super(VIP, self).__init__(parent=app)
        self._app = app
        self.user = user
        self.ui = UI(self._app)