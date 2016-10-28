#coding:utf-8
from .ui import UI

from cloudtea.db import api
from cloudtea.widgets import base




class VIP(base.TObject):
    def __init__(self, app, user):
        super(VIP, self).__init__(parent=app)
        self._app = app
        self.user = user
        self.ui = UI(self._app)
        self.init_signal_binding()

    def init_signal_binding(self):
        self.ui.vip_item.clicked.connect(self.ready_show_desktop)
        self.ui.refresh_btn.clicked.connect(self.ready_show_data)
        self.ui.search_box.returnPressed.connect(self.ready_to_search)
        self.ui.newvip_btn.clicked.connect(self.ready_show_create)
        self.ui.newvip_dialog.ok_btn.clicked.connect(self.ready_to_create)

    def ready_show_desktop(self):
        self._app.ui.central_panel.top_panel.clean()
        self.ready_show_data()

        self._app.ui.central_panel.right_panel.set_widget(self.ui.desktop)
        self._app.ui.central_panel.top_panel.add_item(self.ui.refresh_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.viprecharge_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.newvip_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.search_box, last=True)

    def ready_show_data(self):
        self.ui.desktop.set_data(api.list_vip())

    def ready_to_search(self):
        pass

    def ready_show_create(self):
        self.ui.newvip_dialog.show()

    def ready_to_create(self):
        pass