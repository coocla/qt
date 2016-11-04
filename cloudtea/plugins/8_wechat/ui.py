#coding:utf-8
from cloudtea.widgets import base

class UI(object):
    def __init__(self, app):
        self._app = app


        self.vip_item = base.TGroupItem(self._app, u'微信营销')
        self.vip_item.set_img_text('>')

        self.bind_signal()
        self.setup_ui()

    def setup_ui(self):
        top_panel = self._app.ui.central_panel.top_panel
        side_panel = self._app.ui.side_panel.left_panel

        side_panel.sidebar_panel.add_item(self.vip_item)

    def bind_signal(self):
        self.vip_item.clicked.connect(self.switch_desktop)

    def switch_desktop(self):
        pass
