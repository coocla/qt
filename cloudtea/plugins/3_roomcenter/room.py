#coding:utf-8
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QMessageBox

from .ui import UI
from cloudtea.db import api, utils
from cloudtea.widgets import base


class ROOM(base.TObject):
    def __init__(self, app, user=None):
        super(ROOM, self).__init__(parent=app)
        self._app = app
        self.user = user
        self.ui = UI(self._app)
        self.init_signal_binding()

    def init_signal_binding(self):
        self.ui.room_item.clicked.connect(self.ready_show_desktop)
        self.ui.newroom_btn.clicked.connect(self.ready_show_create)
        self.ui.delroom_btn.clicked.connect(self.ready_to_delete)
        self.ui.refresh_btn.clicked.connect(self.ready_show_data)
        self.ui.newroom_dialog.ok_btn.clicked.connect(self.ready_to_create)

    def ready_show_data(self):
        # 准备桌面数据
        self.ui.desktop.set_data(api.list_room())

    def ready_show_desktop(self):
        self._app.ui.central_panel.top_panel.clean()
        self.ready_show_data()
        # 替换桌面
        self._app.ui.central_panel.right_panel.set_widget(self.ui.desktop)
        # 添加功能按钮
        self._app.ui.central_panel.top_panel.add_item(self.ui.refresh_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.delroom_btn)
        self._app.ui.central_panel.top_panel.add_item(self.ui.newroom_btn)

    def ready_show_create(self):
        self.ui.newroom_dialog.show()

    def ready_to_delete(self):
        index=self.ui.desktop.currentIndex().row()
        Msg = base.Message('warning', self._app)
        if index < 0:
            Msg.show(u'错误', u'请先选中要删除的房间')
        else:
            session = utils.get_session()
            selected = self.ui.desktop.data[index]
            room = api.get_room(selected.id, session=session)
            if not room:
                Msg.show(u'错误', u'选中的房间已经不存在了,刷新在看看?')
            else:
                reply = Msg.show(u'警告', u'你确定要删除房间 [%s] ?' % room.name, confirm=True)
                if reply == QMessageBox.Yes:
                    if room.inused:
                        Msg.show(u'错误', u'房间 [%s] 正在使用中,不允许删除!' % room.name)
                    else:
                        room, _err = room.delete(session)
                        if _err:
                            Msg.show(u'错误', u'删除失败: %s' % _err)
                        else:
                            Msg = base.Message('information', self._app)
                            Msg.show(u'成功', u'房间删除成功!')
                            self.ui.desktop.removeRow(index)


    def ready_to_create(self):
        Msg = base.Message('warning', self._app)
        p = self.ui.newroom_dialog
        if not (p.room_name.text() and p.room_vip_price.text() and p.room_common_price.text() and p.room_capacity.text()):
            Msg.show(u'错误', u'请将所有信息填写完整!')
        try:
            int(p.room_vip_price.text())
            int(p.room_common_price.text())
            int(p.room_capacity.text())
        except:
            Msg.show(u'错误', u'房费和容量要填写为纯数字!')
        pk, _err = api.create_room(self.user, p.room_name.text().encode('utf-8'), p.room_vip_price.text(), p.room_common_price.text(), p.room_capacity.text())
        if _err:
            Msg.show(u'错误', u'数据库错误: %s' % _err)
        else:
            Msg = base.Message('information', self._app)
            Msg.show(u'成功', u'房间添加成功!')
            room = api.get_room(pk)
            print(type(room.name))
            self.ui.desktop.add_item(room)
            p.setParent(None)