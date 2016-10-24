#coding:utf-8
from .ui import UI
from cloudtea.widgets import base


class Sale(base.TObject):
    def __init__(self, app):
        super(Sale, self).__init__(parent=app)
        self._app = app
        self.ui = UI(self._app)