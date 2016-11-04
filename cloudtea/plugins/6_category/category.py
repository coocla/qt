#coding:utf-8
from PyQt5.QtWidgets import QMessageBox

from .ui import UI

from cloudtea.db import api, utils
from cloudtea.widgets import base


class CategoryManage(base.TObject):
    def __init__(self, app, user):
        super(CategoryManage, self).__init__(parent=app)
        self._app = app
        self.user = user
        self.ui = UI(self._app)

        self.init_signal_binding()

    def init_signal_binding(self):
        self.ui.category_item.clicked.connect(self.ready_show_desktop)
        self.ui.refresh_btn.clicked.connect(self.ready_show_data)
        self.ui.search_box.returnPressed.connect(self.ready_to_search)
        self.ui.delcategory_btn.clicked.connect(self.ready_to_delete)
        self.ui.newcategory_btn.clicked.connect(self.ready_show_category)
        self.ui.newcategory_dialog.ok_btn.clicked.connect(self.ready_create_category)

    def ready_show_desktop(self):
        self._app.message('提醒: 已切换至 货品分类 菜单')
        self._app.ui.central_panel.top_panel.clean()
        self.ready_show_data()
        self._app.ui.central_panel.right_panel.set_widget(self.ui.desktop)
        self._app.ui.central_panel.top_panel.add_item(self.ui.refresh_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.delcategory_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.newcategory_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.search_box, last=True)

    def ready_show_data(self):
        self.ui.desktop.set_data(api.list_category())

    def ready_to_search(self):
        text = self.ui.search_box.text()
        data = api.search_category(text)
        self.ui.desktop.set_data(data)

    def ready_to_delete(self):
        index=self.ui.desktop.currentIndex().row()
        Msg = base.Message('warning', self.ui.newcategory_dialog)
        if index < 0:
            Msg.show(u'错误', u'请先选中要删除的分类!')
        else:
            session = utils.get_session()
            selected = self.ui.desktop.data[index]
            category = api.get_category(selected.id, session=session)
            if not category:
                Msg.show(u'错误', u'选中的分类已经不存在了, 刷新下在看看?')
            else:
                reply = Msg.show(u'警告', u'你确定要删除货品 [%s] ?' % category.name, confirm=True)
                if reply == QMessageBox.Yes:
                    if category.inventory:
                        Msg.show(u'警告', u'该分类下还有货品存在,不能删除!')
                    else:
                        category, _err = category.delete(session)
                        if _err:
                            Msg.show(u'错误', u'删除失败: %s' % _err)
                        else:
                            Msg = base.Message('information', self.ui.newcategory_dialog)
                            Msg.show(u'成功', u'分类删除成功!')
                            self.ui.desktop.removeRow(index)

    def ready_show_category(self):
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
                self.ui.desktop.add_item(category)
                self.ui.newcategory_dialog.hide()
