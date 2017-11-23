#! -*- coding:utf-8 -*-

from PyQt5.QtCore import QAbstractTableModel,Qt,QVariant
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.Qt import QTableWidget,QHeaderView,QTableWidgetItem,QNetworkAccessManager,QNetworkRequest,QLineEdit

class MyTableModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
 
    def rowCount(self, parent=None): 
        return len(self.arraydata) 
 
    def columnCount(self, parent=None): 
        try:
            lex = len(self.arraydata[0])
            return lex
        except Exception:
            return 0
 
    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        return QVariant(self.arraydata[index.row()][index.column()]) 

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()        


class RequestsTable(QTableWidget):
    header = ["url", "status", "content-type"]

    def __init__(self):
        super(RequestsTable, self).__init__()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(self.header)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setResizeMode(QHeaderView.ResizeToContents)

    def update(self, data):
        last_row = self.rowCount()
        next_row = last_row + 1
        self.setRowCount(next_row)
        for col, dat in enumerate(data, 0):
            if not dat:
                continue
            self.setItem(last_row, col, QTableWidgetItem(dat))


class Manager(QNetworkAccessManager):
    def __init__(self, table):
        QNetworkAccessManager.__init__(self)
        self.finished.connect(self._finished)
        self.sslErrors.connect(self._ssl_errors)
        self.table = table
#       解决ssl加密套接字问题，很重要  
    def _ssl_errors(self,reply,errors):
        reply.ignoreSslErrors()
        for e in errors:
            print('Ignored SSL Error:{0}-{1}'.format(e.error(),e.errorString()))

    def _finished(self, reply):
        """Update table with headers, status code and url.
        """
        headers = reply.rawHeaderPairs()
        headers = {str(k):str(v) for k,v in headers}
        content_type = headers.get("Content-Type")
        url = reply.url().toString()
        # getting status is bit of a pain
        status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        status, ok = status.toInt()
        self.table.update([url, str(status), content_type])



class MyPage(QWebPage):
    def __init__(self, parent=None):
        super(MyPage, self).__init__(parent)

    def triggerAction(self, action, checked=False):
        if action == QWebPage.OpenLinkInNewWindow:
            self.createWindow(QWebPage.WebBrowserWindow)

        return super(MyPage, self).triggerAction(action, checked)