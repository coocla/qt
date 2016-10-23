#coding:utf-8
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from .ui import UI
from cloudtea.widgets import base


class ROOM(base.TObject):
    def __init__(self, app, user=None):
        super(ROOM, self).__init__(parent=app)
        self._app = app
        self.user = user
        self.ui = UI(self._app)
        self.init_signal_binding()

    def init_signal_binding(self):
        self.ui.create_btn.clicked.connect(self.ready_to_create)

    def ready_to_create(self):
        self.ui.create_dialog.show()


