# -*- coding: utf-8 -*- 

from wsgiref.simple_server import make_server
from cgi import parse_qs

from utils.settings import Setting

from PyQt5.QtCore import QThread
from PyQt5 import QtCore
import urllib.parse

class Listen_to_web(QThread):
    listWidgetAddItem = QtCore.pyqtSignal(dict)
    rowPositionChangeTo = QtCore.pyqtSignal('QString')
    rowPositionChangeToSecond = QtCore.pyqtSignal(list)
    rowPositionChangeToThird = QtCore.pyqtSignal(int,dict,bool)
    
    def __init__(self,pa, parent=None):
        QThread.__init__(self,parent)
        self.pa = pa
#         self.t1.setDaemon(True)
#         self.t1.start()
    
    def application(self,environ, start_response):
        if environ.get('PATH_INFO', 'no')==Setting.internetPath:
            self.handleFieldAndDataReq(environ)
            
        response_body = 'good afternoon'
        status = '200 OK'
        response_headers = [('Content-Type', 'text/plain;charset=utf-8'),]
    
        start_response(status, response_headers)
        return [response_body.encode("utf-8")]
    
    def handleFieldAndDataReq(self,environ):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        request_body = str(request_body,'utf-8')
        d = parse_qs(str(request_body))
        col_index = 0
        rowPosition = self.pa.tableWidget.rowCount()
        self.pa.tableWidget.insertRow(rowPosition)
#         self.pa.tableWidget.setItem(rowPosition,col_index,QTableWidgetItem(u'字段'))
#         my_column_index = col_index
        col_index += 1
        temWebData = {}
        for k in d:
            try:
                temWebData[k]  = urllib.parse.unquote(d[k][0])
            except Exception as u:
                pass
#             try:
#                 temWebData[k]  = (d[k][0])
#             except Exception as u:
#                 temWebData[k]  = (d[k][0].decode('gbk','replace'))
                
        self.rowPositionChangeToSecond.emit([rowPosition,0,temWebData.get('elementTag','')])
        
        scrollYes=True
        self.rowPositionChangeToThird.emit(rowPosition,temWebData,scrollYes)
        self.rowPositionChangeTo.emit(str(rowPosition))
        
    
    
    
    def start_listen_req(self):
        httpd = make_server('0.0.0.0', 9997, self.application)
        httpd.serve_forever()
        
        
    def run(self):
        self.start_listen_req()
        
if __name__=='__main__':
    Listen_to_web()