#coding:utf-8
from PyQt5.QtWidgets import QMessageBox

from .ui import UI

from cloudtea.db import api, utils
from cloudtea.widgets import base 


class User(base.TObject):
    def __init__(self, app, user):
        super(User, self).__init__(parent=app)
        self._app = app
        self.user = user
        self.ui = UI(self._app)

        self.init_signal_binding()

    def init_signal_binding(self):
        self.ui.user_item.clicked.connect(self.ready_show_desktop)
        self.ui.newuser_btn.clicked.connect(self.ready_show_create)
        self.ui.deluser_btn.clicked.connect(self.ready_to_delete)
        self.ui.refresh_btn.clicked.connect(self.ready_show_data)
        self.ui.newuser_dialog.ok_btn.clicked.connect(self.ready_to_create)
        self.ui.search_box.returnPressed.connect(self.ready_to_search)

        self.ui.newuser_dialog.username.editingFinished.connect(self.verify_username)
        self.ui.newuser_dialog.password_confirm.editingFinished.connect(self.verify_password)

    def ready_show_data(self):
        self.ui.desktop.set_data(api.list_user())

    def ready_show_desktop(self):
        self._app.ui.central_panel.top_panel.clean()
        self.ready_show_data()
        self._app.ui.central_panel.right_panel.set_widget(self.ui.desktop)

        self._app.ui.central_panel.top_panel.add_item(self.ui.refresh_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.deluser_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.newuser_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.search_box, last=True)

    def ready_show_create(self):
        self.ui.newuser_dialog.show()

    def ready_to_delete(self):
        index=self.ui.desktop.currentIndex().row()
        Msg = base.Message('warning', self.ui.newuser_dialog)
        if index < 0:
            Msg.show(u'错误', u'请先选中要删除的店员')
        else:
            session = utils.get_session()
            selected = self.ui.desktop.data[index]
            user = api.get_user(selected.id, session=session)
            if not user:
                Msg.show(u'错误', u'选中的店员已经不存在了,刷新在看看?')
            else:
                reply = Msg.show(u'警告', u'你确定要删除店员 [%s] ?' % user.name, confirm=True)
                if reply == QMessageBox.Yes:
                    user, _err = user.delete(session)
                    if _err:
                        Msg.show(u'错误', u'删除失败: %s' % _err)
                    else:
                        Msg = base.Message('information', self.ui.newuser_dialog)
                        Msg.show(u'成功', u'店员删除成功!')
                        self.ui.desktop.removeRow(index)

    def ready_to_create(self):
        Msg = base.Message('warning', self.ui.newuser_dialog)
        p = self.ui.newuser_dialog
        if not (p.name.text() and p.username.text() and p.password.text() and p.age.text() and p.password_confirm.text() and 
            p.sex.currentText() and p.phone.text()):
            Msg.show(u'错误', u'请将信息填写完整!')
        else:
            pk, _err = api.create_user(self.user, p.name.text(), p.username.text(), p.password.text(), p.sex.currentText(), p.age.text(), p.phone.text(), p.role.currentIndex())
            if _err:
                Msg.show(u'错误', u'数据库错误: %s' % _err)
            else:
                Msg = base.Message('information', self.ui.newuser_dialog)
                Msg.show(u'成功', u'店员添加成功!')
                user = api.get_user(pk)
                self.ui.desktop.add_item(user)
                p.hide()

    def ready_to_search(self):
        text = self.ui.search_box.text()
        data = api.search_user(text)
        self.ui.desktop.set_data(data)

    def verify_username(self):
        Msg = base.Message('warning', self.ui.newuser_dialog)
        text = self.ui.newuser_dialog.username.text()
        if api.verify_username(text):
            Msg.show(u'错误', u'账户 [%s] 已经被占用,换个其他的试试?' % text)

    def verify_password(self):
        p1 = self.ui.newuser_dialog.password.text()
        p2 = self.ui.newuser_dialog.password_confirm.text()
        Msg = base.Message('warning', self.ui.newuser_dialog)
        if p1 != p2:
            Msg.show(u'错误', u'两次输出的密码不一致!')
        else:
            if len(p2) < 6:
                Msg.show(u'错误', u'密码长度至少6位以上,包含6位')
