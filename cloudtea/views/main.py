#coding:utf-8
import qtawesome as qta

from PySide.QtGui import *

from cloudtea.views import users, rooms, widgets

class MainWindow(QMainWindow):
    def __init__(self, context=None):
        super(MainWindow, self).__init__()
        self.context = context
        self.initUI()

    def initUI(self):
        self.initMenu()
        self.initStatusBar()
        self.initToolBar()
        self.resizeWindow()

        widget = QWidget()
        self.setCentralWidget(widget)
        self.hbox = QVBoxLayout()
        self.btn_box = QHBoxLayout()

        self.hbox.addLayout(self.btn_box)
        self.initWidget()

        self.initFunBtnSet()

        self.centralWidget().setLayout(self.hbox)

    def initMenu(self):
        file_action = QAction(QIcon(), u'打开文件', self)

        menubar = self.menuBar()
        file_menu = menubar.addMenu(u'文件')
        user_menu = menubar.addMenu(u'店员管理')
        vip_menu = menubar.addMenu(u'会员管理')
        inventory_menu = menubar.addMenu(u'库存管理')
        store_menu = menubar.addMenu(u'店铺管理')
        data_graph = menubar.addMenu(u'报表分析')
        sys_menu = menubar.addMenu(u'系统设置')
        help_menu = menubar.addMenu(u'关于')

        file_menu.addAction(file_action)

    def initStatusBar(self):
        self.statusBar().showMessage(u'就绪	')

    def initToolBar(self):
        openroom = QAction(QIcon(),u'开房间',self)
        endbalance = QAction(QIcon(),u'结账',self)
        vip_recharge = QAction(QIcon(),u'开通会员',self)
        vip_create = QAction(QIcon(),u'会员充值',self)

        self.openroom = self.addToolBar('openroom')
        self.endbalance = self.addToolBar('endbalance')
        self.vip_create = self.addToolBar('vip_create')
        self.vip_recharge = self.addToolBar('vip_recharge')

        self.openroom.addAction(openroom)
        self.endbalance.addAction(endbalance)
        self.vip_create.addAction(vip_create)
        self.vip_recharge.addAction(vip_recharge)

    def resizeWindow(self):
        self.setGeometry(300, 300, 1024, 600)
        self.setWindowTitle(u'浮云茶舍')
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initWidget(self):
        table = QTableView()
        mapped = [
            {"name":"name", "display":u"姓名"},
            {"name":"username","display":u"账号"},
            {"name":"sex","display":u"性别"},
            {"name":"age","display":u"年龄"},
            {"name":"phone","display":u"联系方式"},
            {"name":"created_at","display":u"添加时间"}
        ]
        hiden = ('id', 'password', 'role')

        model = widgets.BaseTableView('users', mapped, hiden)
        table.setModel(model)
        table.setItemDelegate(users.UserDelegate())
        header = table.horizontalHeader()
        header.setMovable(True)
        for index, field in enumerate(mapped):
            if index+1 == len(mapped):
                continue
            header.swapSections(model.fieldIndex(field['name']), index)

        table.setEditTriggers(QAbstractItemView.NoEditTriggers) #不允许编辑
        table.setSortingEnabled(True)    #开启排序
        table.resizeColumnsToContents()  #列宽自适应内容
        header.setStretchLastSection(True)  #最后一列充满窗口
        self.hbox.addWidget(table)

    def initFunBtnSet(self):
        btn_newuser = QPushButton(u'新增用户', self)
        btn_newsearch = QPushButton(u'搜索', self)
        btn_newuser.clicked.connect(self._on_userbtn_clicked)
        self.dialog = users.NewUserDialog()
        self.btn_box.addWidget(btn_newuser)
        self.btn_box.addWidget(btn_newsearch)
        self.btn_box.addStretch()

    def _on_userbtn_clicked(self):
        self.dialog.exec_()