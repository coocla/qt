#coding:utf-8
from .ui import UI
from cloudtea.widgets import base


class DataCenter(base.TObject):
    def __init__(self, app, user):
        super(DataCenter, self).__init__(parent=app)
        self._app = app
        self.ui = UI(self._app)