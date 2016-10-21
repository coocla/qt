#coding:utf-8
from cloudtea.widgets import base


class VIP(base.TObject):
    def __init__(self, app):
        super(VIP, self).__init__(parent=app)
        self._app = app