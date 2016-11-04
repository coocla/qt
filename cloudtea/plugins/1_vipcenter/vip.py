#coding:utf-8
from PyQt5.QtWidgets import QMessageBox

from .ui import UI

from cloudtea.db import api, utils
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
        self.ui.delvip_btn.clicked.connect(self.ready_to_delete)
        self.ui.newvip_dialog.ok_btn.clicked.connect(self.ready_to_create)
        self.ui.newvip_dialog.vip_id.editingFinished.connect(self.verify_vip_id)


    def ready_show_desktop(self):
        self._app.message('提醒: 已切换至 会员管理 菜单')
        self._app.ui.central_panel.top_panel.clean()
        self.ready_show_data()

        self._app.ui.central_panel.right_panel.set_widget(self.ui.desktop)
        self._app.ui.central_panel.top_panel.add_item(self.ui.refresh_btn)
        if self.user.role == 0 or self.user.id == 1:
            self._app.ui.central_panel.top_panel.add_item(self.ui.delvip_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.viprecharge_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.newvip_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.search_box, last=True)

    def ready_show_data(self):
        self.ui.desktop.set_data(api.list_vip())

    def ready_to_search(self):
        text = self.ui.search_box.text()
        data = api.search_vip(text)
        self.ui.desktop.set_data(data)

    def ready_show_create(self):
        self.ui.newvip_dialog.show()

    def ready_to_delete(self):
        index=self.ui.desktop.currentIndex().row()
        Msg = base.Message('warning', self.ui.newvip_dialog)
        if index < 0:
            Msg.show(u'错误', u'请先选中要删除的会员')
        else:
            session = utils.get_session()
            selected = self.ui.desktop.data[index]
            vip = api.get_vip(selected.id, session=session)
            if not vip:
                Msg.show(u'错误', u'选中的会员已经不存在了,刷新在看看?')
            else:
                reply = Msg.show(u'警告', u'你确定要删除会员 [%s] ?' % vip.name, confirm=True)
                if reply == QMessageBox.Yes:
                    if vip.amount:
                        Msg.show(u'错误', u'会员 [%s] 卡中还有余额,不允许删除!' % vip.name)
                    else:
                        vip, _err = vip.delete(session)
                        if _err:
                            Msg.show(u'错误', u'删除失败: %s' % _err)
                        else:
                            Msg = base.Message('information', self.ui.newvip_dialog)
                            Msg.show(u'成功', u'会员删除成功!')
                            self.ui.desktop.removeRow(index)

    def ready_to_create(self):
        Msg = base.Message('warning', self.ui.newvip_dialog)
        p = self.ui.newvip_dialog
        if not (p.name.text() and p.vip_id.text() and p.amount.text() and p.phone.text()):
            Msg.show(u'错误', u'请将信息填写完整!')
        else:
            pk, _err = api.create_vip(self.user, p.name.text(), p.vip_id.text(), p.amount.text(), p.phone.text())
            if _err:
                Msg.show(u'错误', u'数据库错误: %s' % _err)
            else:
                Msg = base.Message('information', self.ui.newvip_dialog)
                Msg.show(u'成功', u'会员添加成功!')
                vip = api.get_vip(pk)
                self.ui.desktop.add_item(vip)
                p.hide()

    def verify_vip_id(self):
        Msg = base.Message('warning', self.ui.newvip_dialog)
        text = self.ui.newvip_dialog.vip_id.text()
        if api.get_vip(text):
            Msg.show(u'错误', u'VIP ID [%s] 已经被占用,换个其他的试试?' % text)

