#coding:utf-8
from .ui import UI

from cloudtea.db import api
from cloudtea.widgets import base


class Inventory(base.TObject):
    def __init__(self, app, user):
        super(Inventory, self).__init__(parent=app)
        self._app = app
        self.user = user
        self.ui = UI(self._app)

        self.init_signal_binding()

    def init_signal_binding(self):
        self.ui.inventory_item.clicked.connect(self.ready_show_desktop)
        self.ui.refresh_btn.clicked.connect(self.ready_show_data)
        self.ui.search_box.returnPressed.connect(self.ready_to_search)

    def ready_show_desktop(self):
        self._app.ui.central_panel.top_panel.clean()
        self.ready_show_data()
        self._app.ui.central_panel.right_panel.set_widget(self.ui.desktop)
        self._app.ui.central_panel.top_panel.add_item(self.ui.refresh_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.delinventory_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.newinventory_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.search_box, last=True)

    def ready_show_data(self):
        self.ui.desktop.set_data(api.list_inventory())

    def ready_to_search(self):
        text = self.ui.search_box.text()
        data = api.search_inventory(text)
        self.ui.desktop.set_data(data)