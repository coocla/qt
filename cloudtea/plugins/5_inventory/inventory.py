#coding:utf-8
from PyQt5.QtWidgets import QMessageBox

from .ui import UI

from cloudtea.db import api, utils
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
        self.ui.delinventory_btn.clicked.connect(self.ready_to_delete)
        self.ui.newinventory_btn.clicked.connect(self.ready_show_create)
        self.ui.newinventory_dialog.ok_btn.clicked.connect(self.ready_to_create)

        self.ui.newinventory_dialog.category.currentIndexChanged.connect(self.ready_show_category)
        self.ui.newcategory_dialog.ok_btn.clicked.connect(self.ready_create_category)

    def ready_show_desktop(self):
        self._app.message('提醒: 已切换至 库存管理 菜单')
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

    def ready_to_delete(self):
        index=self.ui.desktop.currentIndex().row()
        Msg = base.Message('warning', self.ui.newinventory_dialog)
        if index < 0:
            Msg.show(u'错误', u'请先选中要删除的货品!')
        else:
            session = utils.get_session()
            selected = self.ui.desktop.data[index]
            inventory = api.get_inventory(selected.id, session=session)
            if not inventory:
                Msg.show(u'错误', u'选中的货品已经不存在了, 刷新下在看看?')
            else:
                reply = Msg.show(u'警告', u'你确定要删除货品 [%s] ?' % inventory.name, confirm=True)
                if reply == QMessageBox.Yes:
                    if inventory.oversale:
                        Msg.show(u'警告', u'该货品还有会员在店内存留,不能删除!')
                    else:
                        inventory, _err = inventory.delete(session)
                        if _err:
                            Msg.show(u'错误', u'删除失败: %s' % _err)
                        else:
                            Msg = base.Message('information', self.ui.newinventory_dialog)
                            Msg.show(u'成功', u'货品删除成功!')
                            self.ui.desktop.removeRow(index)

    def ready_show_create(self):
        self.ui.newinventory_dialog.category.insertItem(0, '--- 货品分类 ---')
        self.ui.newinventory_dialog.category.insertItem(1, '................新增货品分类')
        for item in api.list_category():
            self.ui.newinventory_dialog.category.addItem(item.name)
        self.ui.newinventory_dialog.show()

    def ready_to_create(self):
        Msg = base.Message('warning', self.ui.newcategory_dialog)
        p = self.ui.newinventory_dialog
        if p.category.currentIndex() == 0 or p.category.currentIndex() == 1:
            Msg.show(u'错误', u'请选择货品分类!')
        else:
            if not (p.name.text() and p.specifications.text() and p.category.currentIndex() and p.number.text() and \
                p.meter.currentIndex() and p.price.text() and p.suttle.text()):
                Msg.show(u'错误', u'请将货品信息填写完整!')
            else:
                category = api.get_category(p.category.currentText())
                pk, _err = api.create_inventory(self.user, p.name.text(), p.specifications.text(), p.number.text(), p.meter.currentIndex()-1, \
                    p.price.text(), p.suttle.text(), category.id)
                if _err:
                    Msg.show(u'错误', u'数据库错误: %s' % _err)
                else:
                    Msg = base.Message('information', self.ui.newinventory_dialog)
                    Msg.show(u'成功', u'货品添加成功')
                    inventory = api.get_inventory(pk)
                    self.ui.desktop.add_item(inventory)
                    p.hide()

    def ready_show_category(self):
        if self.ui.newinventory_dialog.category.currentIndex() == 1:
            self.ui.newcategory_dialog.show()

    def ready_create_category(self):
        Msg = base.Message('warning', self.ui.newcategory_dialog)
        text = self.ui.newcategory_dialog.name.text()
        if api.get_category(text):
            Msg.show(u'错误', u'分类 [%s] 已经存在!' % text)
        else:
            pk, _err = api.create_category(self.user, text)
            if _err:
                Msg.show(u'错误', u'数据库错误: %s' % _err)
            else:
                Msg = base.Message('information', self.ui.newcategory_dialog)
                Msg.show(u'成功', u'货品分类添加成功!')
                category = api.get_category(pk)
                self.ui.newinventory_dialog.category.addItem(category.name)
                index=self.ui.newinventory_dialog.category.findText(category.name)
                self.ui.newinventory_dialog.category.setCurrentIndex(index)
                self.ui.newcategory_dialog.hide()
