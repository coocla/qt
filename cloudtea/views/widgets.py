#coding:utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *

class BaseWidget(QWidget):
    def __init__(self):
        super(BaseWidget,self).__init__()
        self.move_center()

    def move_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def BaseTableView(table, mapped, hidens=()):
    model = QSqlTableModel()
    model.setTable(table)
    if (model.select()):
        for hiden in hidens:
            model.removeColumn(model.fieldIndex(hiden))
        for field in mapped:
            model.setHeaderData(model.fieldIndex(field['name']), Qt.Horizontal, field['display'])
    return model

class Pagination(QWidget):
    def __init__(self, model):
        super(Pagination,self).__init__()
        self.SinglePageNum = 1
        self.CurrentPageNum = 0
        self.model = model

        self.box = QHBoxLayout()

        self.prebtn = QPushButton(u'上一页', self)
        self.nextbtn = QPushButton(u'下一页', self)
        self.switchbtn = QPushButton(u'Go', self)

        self.switch_start = QLabel(u'转到第')
        self.switch_end = QLabel(u'页')

        self.totalcount = QLabel()
        self.totalpage = QLabel()
        self.singlepage = QLabel()
        self.currentpage = QLabel()

        self.switchpage = QLineEdit()

        self.initSignal()
        self.initWindow()
        self.QueryRecord(self.CurrentPageNum)
        self.UpdateStatus()
        self.setLayout(self.box)

    def initSignal(self):
        self.prebtn.clicked.connect(self.On_PreBtn_Clicked)
        self.nextbtn.clicked.connect(self.On_NextBtn_Clicked)
        self.switchbtn.clicked.connect(self.On_SwitchBtn_Clicked)

    def initWindow(self):
        self.box.addWidget(self.totalpage)
        self.box.addWidget(self.currentpage)
        self.box.addWidget(self.totalcount)
        self.box.addWidget(self.singlepage)
        self.box.addStretch()
        self.box.addWidget(self.prebtn)
        self.box.addWidget(self.nextbtn)
        self.box.addWidget(self.switch_start)
        self.box.addWidget(self.switchpage)
        self.box.addWidget(self.switch_end)
        self.box.addWidget(self.switchbtn)

    def On_PreBtn_Clicked(self):
        self.CurrentPageNum -= 1
        if self.CurrentPageNum < 0:
            self.CurrentPageNum = 0
        self.QueryRecord(self.CurrentPageNum)
        self.UpdateStatus()

    def On_NextBtn_Clicked(self):
        self.CurrentPageNum += 1
        if self.CurrentPageNum > self.TotalPageCount():
            self.CurrentPageNum = self.TotalPageCount()
        self.QueryRecord(self.CurrentPageNum)
        self.UpdateStatus()

    def On_SwitchBtn_Clicked(self):
        pagenum = self.switchpage.text()
        try:
            pagenum = int(pagenum)
        except Exception as e:
            QMessageBox.information(self, u'提示', u'请输入数字')
            return
        self.CurrentPageNum = pagenum - 1
        if self.CurrentPageNum > self.TotalPageCount():
            self.CurrentPageNum = self.TotalPageCount()
        if self.CurrentPageNum < 0:
            self.CurrentPageNum = 0
        self.QueryRecord(self.CurrentPageNum)
        self.UpdateStatus()

    def TotalRecord(self):
        '''
        总条数
        '''
        #self.model.setQuery('select count(*) from %s' % self.table)
        #self.TotalNum = self.model.record(0).value(0)
        self.TotalNum = self.model.rowCount()
        return self.TotalNum

    def TotalPageCount(self):
        '''
        总页数
        '''
        if self.TotalNum % self.SinglePageNum:
            return self.TotalNum/self.SinglePageNum + 1
        return self.TotalNum/self.SinglePageNum

    def UpdateStatus(self):
        self.currentpage.setText(u'当前第%s页' % str(self.CurrentPageNum+1))
        self.totalcount.setText(u'总共%s条' % str(self.TotalRecord()))
        self.singlepage.setText(u'单页显示%s条' % str(self.SinglePageNum))
        self.totalpage.setText(u'总共%s页' % str(self.TotalPageCount()))
        self.switchpage.setFixedWidth(40)
        if self.CurrentPageNum == 0:
            self.prebtn.setEnabled(False)
        else:
            self.prebtn.setEnabled(True)
        if self.TotalPageCount() > self.CurrentPageNum+1:
            self.nextbtn.setEnabled(True)
        else:
            self.nextbtn.setEnabled(False)

    def QueryRecord(self, index):
        offset = index * self.SinglePageNum
        self.model.setFilter('limit %d offset %d' % (self.SinglePageNum, offset))
        self.model.select()
        #self.model.setQuery('select * from %s limit %d,%d' % (self.table, offset, self.SinglePageNum))