#coding:utf-8
import qtawesome as qta

from PySide.QtGui import *

from cloudtea.models import desktop

class MainWindow(QMainWindow):
	def __init__(self, context=None):
		super(MainWindow, self).__init__()
		self.context = context
		self.initUI()

		widget = QWidget()
		self.setCentralWidget(widget)

		hbox = QVBoxLayout()
		hbox.addWidget(self.initWidget())

		self.centralWidget().setLayout(hbox)

	def initUI(self):
		self.initMenu()
		self.initStatusBar()
		self.initToolBar()
		self.resizeWindow()


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
		ds = QTableView()
		ds.setModel(desktop.roomModel())
		ds.setColumnHidden(0, True)
		ds.setEditTriggers(QAbstractItemView.NoEditTriggers) #不允许编辑
		ds.setSortingEnabled(True)    #开启排序
		ds.resizeColumnsToContents()  #列宽自适应内容
		ds.horizontalHeader().setStretchLastSection(True)  #最后一列充满窗口
		return ds