# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.

"""

from PyQt5.QtWidgets import QMainWindow,QMessageBox,QMenu,QInputDialog,QAbstractItemView,QTreeWidgetItem
from PyQt5.QtCore import Qt,pyqtSlot,QUrl,QByteArray
from PyQt5.QtWebKit import QWebSettings
from PyQt5.Qt import QTableWidgetItem
from PyQt5 import QtCore, QtWidgets,QtGui
import utils.auto_test3_image_rc
from lxml import etree
import sys,os,sqlite3,json,codecs,time,re,types,requests
_translate = QtCore.QCoreApplication.translate


from main.Ui_zicada import Ui_MainWindow
from main.modifyConfig import ModifyDialog
from login.login import LoginDialog
from utils.table_init import InitTable
from utils.optionWeb import MyPage
from utils.my_js import MyJs
from f2b2f.handle_chrome_web import Listen_to_web
from main.addCoffee import AddCoffeeDialog
from main.ipConfig import IpConfigDialog
from main.modifyXPath import ModifyXpathDialog
from main.pageSet import PageSetDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.bananaIndex = 1
        self.tabWidget.removeTab(0)
        
        #初始化用户
        self.readyToExport = []
        self.dbpath = InitTable.dbpath
        self.initCurrentUser()
        
        self.showLoadingGif()
        self.init_socket()
        #为tab绑定关闭信号
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        #为tree绑定右击信号
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.treeWidget.customContextMenuRequested.connect(self.rightClickTree) 
        #初始化数据树
        self.init_tree()
        
        self.initWebView()
        self.initTableView()
        
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
#         now_index =  self.stackedWidget.currentIndex() +1 
#         self.stackedWidget.setCurrentIndex(now_index)
#         self.internet_addr = 'http://xycz.chizhou.gov.cn/credit-website/publicity/public/red-name-list.do?navId=3F075D94AE882710E0501FAC12017CC9&columnId=3F075D94AE892710E0501FAC12017CC9';
#         self.webView.load(QUrl(self.internet_addr))
#         self.movie.start()
#         if self.labels.isHidden():
#             self.labels.setHidden(False)
            
            
        selectedTheme = '&'.join([(self.comboBox.currentText()),(self.comboBox.itemData(self.comboBox.currentIndex()))])
        selectedCoffee = '&'.join([(self.comboBox_2.currentText()),(self.comboBox_2.itemData(self.comboBox_2.currentIndex()))])
        selectedTaskName = (self.lineEdit.text())
        if not selectedTaskName:
            QMessageBox.information(self, u'提示', u'任务不能为空') 
            return
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            #获取当前任务的id
            ids = c.execute(InitTable.get_local_id,(self.configId,self.currentTaskName,self.currentTaskCoffee,self.currentTaskTheme,self.username))
            nowTaskId = [d[0] for d in ids]
            #更新数据库中的task任务
            if len(nowTaskId):
                self.currentTaskId = nowTaskId[0]
                c.execute(InitTable.update_local_task,(selectedTaskName,selectedCoffee,selectedTheme,self.currentTaskId,))
                conn.commit()
            else:
                raise Exception(u"id不存在，需要新建任务")
        except Exception as a:
            #插入一条任务
            serialName = str(int(time.mktime(time.gmtime())))
            c.execute(InitTable.insert_new_task_data,(serialName,selectedTaskName,selectedCoffee,selectedTheme,self.username,self.configId,))
            self.currentTaskId = c.lastrowid
            self.currentLink = None
#             self.lineEdit_9.setText('')
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "任务:%s" %selectedTaskName, None))
        finally:
            conn.commit()
            conn.close()            
         
        self.currentTaskName = selectedTaskName
        self.currentTaskCoffee = selectedCoffee
        self.currentTaskTheme = selectedTheme
        
        #每一次都要更新树的结构
        self.re_inint_tree()
        #全部展开
#         self.treeWidget.expandToDepth(1)
        self.checkInternetAndReplaceButton33()
        
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        被选中的主题
        """
        text = '&'.join([(self.comboBox.itemText(index)),(self.comboBox.itemData(index))])
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        my_coffee_combo = c.execute(InitTable.get_local_coffee_exclude_parent_id,(self.configId,(text),self.username))
        self.comboBox_2.clear()
        for cof in my_coffee_combo:
            conff_split = cof[1].split('&')
            self.comboBox_2.addItem(conff_split[0],conff_split[1])

    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        插入要选择的页面方式
        """
        apple = list()
        apple.append(u'登录页')
        apple.append(u'列表或表格页')
        apple.append(u'翻页')
        apple.append(u'详情页')
        
        orange = []
        orange.append('login')
        orange.append('listOrTable')
        orange.append('nextPage')
        orange.append('detail')
        
        appleValue, ok = QInputDialog.getItem(self, u'选择操作环节', u'请选择', apple,current=1,editable = False)
        
        if ok:
            appleIndex = apple.index(appleValue)
            orangeValue = orange[appleIndex]
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            
            newItem = QTableWidgetItem()
            newItem.setBackground(QtGui.QColor(0,255,0))
            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            self.tableWidget.setItem(rowPosition,0,newItem)
            
            newItem = QTableWidgetItem(appleValue)
            newItem.setBackground(QtGui.QColor(0,255,0))
            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            self.tableWidget.setItem(rowPosition,1,newItem)
            
            newItem = QTableWidgetItem(orangeValue)
            newItem.setBackground(QtGui.QColor(0,255,0))
            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            self.tableWidget.setItem(rowPosition,2,newItem)
            
            newItem = QTableWidgetItem(str(self.bananaIndex))
            newItem.setBackground(QtGui.QColor(0,255,0))
            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            self.tableWidget.setItem(rowPosition,3,newItem)
            self.bananaIndex += 1
            
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
        self.bananaIndex = 1
        
    
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        ok = QMessageBox.question(self, u'关闭', u'要关闭当前页面吗？',QMessageBox.Yes,QMessageBox.No)
        if ok== QMessageBox.Yes:
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.removeRow(0)
            self.bananaIndex = 1
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", u"任务:创建任务", None))
            
            now_index =  self.stackedWidget.currentIndex() - 1
            self.stackedWidget.setCurrentIndex(now_index)
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.currentTaskName = None
            
    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        """
        Slot documentation goes here.
        """
#         for row in range(self.tableWidget.rowCount()):
#             self.tableWidget.removeRow(0)
        if self.tableWidget.rowCount():
            self.saveAllDataToSqlite()
            
    
        
    @pyqtSlot()
    def on_actionSynchronizastion_triggered(self):
        """
        Slot documentation goes here.
        数据同步到远程系统中
        """
        if self.configId>0:
            storeExportDatasList = self.exportOrSyncDatas()
            if len(storeExportDatasList):
                syncDataToRemoteSystem = json.dumps(storeExportDatasList)
                headers={'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                syncResult = requests.post(self.syncDataPathStroe,headers=headers,data = syncDataToRemoteSystem)
                if isinstance(syncResult.content,str):
                    syncResultFromRemoteDict = None
                    try:
                        syncResultFromRemote = str(syncResult.content,'utf-8')
                        syncResultFromRemoteDict = json.loads(syncResultFromRemote)
                    except Exception as e:
                        syncResultFromRemote=':'.join(syncResultFromRemote.split('='))
                        syncResultFromRemoteDict = json.loads(syncResultFromRemote)
                    if syncResultFromRemoteDict:
                        syncKeys = syncResultFromRemoteDict.keys()
                        if len(syncKeys):
                            QMessageBox.information(self, u'未同步数据：', ';'.join(syncKeys))
                            
                QMessageBox.information(self, u'数据同步', u'数据同步成功')
            else:
                QMessageBox.information(self, u'提示', u'您未选择需要同步的数据')
        else:
            QMessageBox.information(self, u'提示', u'本地用户无法禁用同步数据')
        
    @pyqtSlot()
    def on_actionExport_triggered(self):
        """
        Slot documentation goes here.
        选定需要导出的task，然后选择此按钮进行导出
        """
        path = QtWidgets.QFileDialog.getSaveFileName(
        self, u'保存文件', '', 'USTC(*.ustc)')
        storeExportDatasList = []
        if len(path)>1 and path[0]:
            with codecs.open(path[0], 'wb',encoding='utf-8') as stream:
                storeExportDatasList = self.exportOrSyncDatas()
                if len(storeExportDatasList):
                    json.dump(storeExportDatasList,stream,ensure_ascii=False)
                    QMessageBox.information(self, u'USTC', u'保存成功')
                else:
                    QMessageBox.information(self, u'提示', u'您未选择需要导出的数据')
    @pyqtSlot()
    def on_actionImport_triggered(self):
        """
        Slot documentation goes here.
        将数据库中的全部数据进行导出
        """
        path = QtWidgets.QFileDialog.getOpenFileName(
        self, u'打开文件', '', 'USTC(*.ustc)')
        
        #记录更新的数据
        recodeUpdateData = []
        #记录更新失败的数据
        recodeUpdateFaild = []
        #记录插入的数据
        recodeInsertData = []
        #记录插入失败的数据
        recodeInsertFaild = []
        #未能更新的数据
        recodeCannotUpdate = []
        
        if len(path)>1 and path[0]:
            with codecs.open((path), 'rb',encoding='utf-8') as stream:
                readDatas =  stream.readlines()
                for taskDatas in readDatas:
                    taskJson = json.loads(taskDatas)
                    recodeUpdateData,recodeInsertData,recodeCannotUpdate = self.importDatasToMySqlite3(taskJson)
            self.init_tree()
            QMessageBox.information(self, u'提示', u'更新{0}:{1};\n插入{2}:{3};\n未更新{4}:{5}'.format(len(recodeUpdateData),' '.join(recodeUpdateData),len(recodeInsertData),' '.join(recodeInsertData),len(recodeCannotUpdate),' '.join(recodeCannotUpdate))) 
                                
    
    @pyqtSlot()
    def on_actionExit_triggered(self):
        """
        Slot documentation goes here.
        退出此系统
        """
        ok = QMessageBox.question(self, u'退出', u'要退出系统是吧？',QMessageBox.Yes,QMessageBox.No)
        if ok== QMessageBox.Yes:
            os._exit(0)
    
    @pyqtSlot()
    def on_actionConfig_param_triggered(self):
        """
        Slot documentation goes here.
        用于进行参数配置
        """
        self.ipConfigDialog = IpConfigDialog()
        self.ipConfigDialog.show()
        

    
    @pyqtSlot()
    def on_actionModify_config_triggered(self):
        """
        Slot documentation goes here.
        用于配置参数的修改
        """
        self.modifyDialog = ModifyDialog()
        self.modifyDialog.show()
    
    @pyqtSlot()
    def on_actionInfo_triggered(self):
        """
        Slot documentation goes here.
        用于展示系统信息
        """
        QMessageBox.aboutQt( self, "PyQt" )
    
    
        
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_itemDoubleClicked(self, item, column):
        """
        Slot documentation goes here.
        用于左侧树中的任务被双击后获取xpath的操作
        """
        if not item.text(2):
            return
        
        task_coffee = item.parent()
        if task_coffee:
            task_theme = task_coffee.parent()
            task_theme = self.getTopTheme(task_theme)
            if task_theme:
                self.currentTaskCoffee = ('&'.join([(task_coffee.text(0)),(task_coffee.text(1))]))
                self.currentTaskTheme = ('&'.join([(task_theme.text(0)),(task_theme.text(1))]))
                self.currentTaskName = (item.text(0))
                ok = QMessageBox.Yes
                if self.stackedWidget.currentIndex():
                    ok = QMessageBox.question(self, u'退出', u'要舍弃当前的配置吗？',QMessageBox.Yes,QMessageBox.No)
                if ok== QMessageBox.Yes:
                    self.bananaIndex = 1
#                     self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
    #                 self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", u"任务:创建任务", None))
                    self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", u"任务:%s" %item.text(0), None))
                    self.tabWidget.setCurrentWidget(self.tab_2)
                    self.tabWidget.setTabEnabled(self.tabWidget.currentIndex(),True)
                    self.stackedWidget.setCurrentIndex(0)
                    self.lineEdit.setText(item.text(0))
                    allThemeItems = ['&'.join([(self.comboBox.itemText(i)),(self.comboBox.itemData(i))]) for i in range(self.comboBox.count())]
                    try:
                        idx_theme = allThemeItems.index('&'.join([(task_theme.text(0)),(task_theme.text(1))]))
                        self.comboBox.setCurrentIndex(idx_theme)
                        
                        conn = sqlite3.connect(self.dbpath)
                        c = conn.cursor()
                        my_coffee_combo = c.execute(InitTable.get_local_coffee_exclude_parent_id,(self.configId,'&'.join([(task_theme.text(0)),(task_theme.text(1))]),self.username))
                        self.comboBox_2.clear()
                        for cof in my_coffee_combo:
                            conf_split = cof[1].split('&')
                            self.comboBox_2.addItem(conf_split[0],conf_split[1])
                        allCoffeeItems = ['&'.join([(self.comboBox_2.itemText(i)),(self.comboBox_2.itemData(i))]) for i in range(self.comboBox_2.count())]
                        idx_coffee = allCoffeeItems.index('&'.join([(task_coffee.text(0)),(task_coffee.text(1))]))
                        self.comboBox_2.setCurrentIndex(idx_coffee)
                    except Exception as e:
                        pass
                        
                    try:
                        #获取当前任务的id
                        ids = c.execute(InitTable.get_local_id,(self.configId,self.currentTaskName,self.currentTaskCoffee,self.currentTaskTheme,self.username))
                        nowTaskId = [d[0] for d in ids]
                        #更新数据库中的task任务
                        if len(nowTaskId):
                            self.currentTaskId = nowTaskId[0]
                        #查询与任务对应的链接，并填充
                        links = c.execute(InitTable.select_task_link,(self.currentTaskId,))
                        lk = [l[0] for l in links]
                        if len(lk):
                            self.currentLink = lk[0]
                            self.lineEdit_2.setText(lk[0])
                        else:
                            self.currentLink = None
                            self.lineEdit_2.setText('')
                    except Exception as a:
                        pass
                        
    #获取树的顶层主题
    def getTopTheme(self,task_theme):
        tem_task_theme = None
        while task_theme:
            tem_task_theme = task_theme
            task_theme = tem_task_theme.parent()
        return tem_task_theme
    
    @pyqtSlot(float)
    def on_doubleSpinBox_valueChanged(self, p0):
        """
        Slot documentation goes here.
        修改浏览器的显示比例
        """
        self.webView.setZoomFactor(p0)
        
    def initWebView(self):
        page = MyPage()
        page.mainFrame().loadFinished.connect(self.onDone)
        self.webView.setPage(page)
#         加载swf文件需要此项设置，很重要
        settings = self.webView.settings()
#         settings.setAttribute(QWebSettings.PluginsEnabled,True) #不能加，否则不能与后台通信
        settings.setAttribute(QWebSettings.LocalStorageDatabaseEnabled,True)
#         self.webView.setZoomFactor(0.65)
        
    def onDone(self,p0):
        if p0:
            self.movie.stop()
            self.labels.setHidden(True)
            frame = self.webView.page().currentFrame()
            frame.evaluateJavaScript((MyJs.js))
        if not p0:
            QMessageBox.information(self, u'提示', u'对不起，加载失败！') 
            
    
        
    def initTableView(self):
        listsHorizontalHeaderItem = [u'操作',u'xpath',u'提取到的数据',u'结果处理方式',u'标签的id',u'标签的class',u'标签的name',u'起始页',u'终止页']
        self.tableWidget.setColumnCount(len(listsHorizontalHeaderItem))
        for index in range(self.tableWidget.columnCount()):
            self.tableWidget.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(listsHorizontalHeaderItem[index]))
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,350)
        self.tableWidget.setColumnWidth(2,350)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(7,20)
        self.tableWidget.setColumnWidth(8,20)
#         self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.tableWidget.customContextMenuRequested.connect(self.showContextMenu)
        
#         self.tableWidget.setColumnHidden(1,True)
        self.tableWidget.setColumnHidden(4,True)
        self.tableWidget.setColumnHidden(5,True)
        self.tableWidget.setColumnHidden(6,True)
        self.tableWidget.setColumnHidden(7,True)
        self.tableWidget.setColumnHidden(8,True)

    def init_socket(self):
        self.listenToWeb = Listen_to_web(self)
        self.listenToWeb.rowPositionChangeTo.connect(self.addColboxToTableView)
        self.listenToWeb.rowPositionChangeToSecond.connect(self.addColboxToTableView_2)
        self.listenToWeb.rowPositionChangeToThird.connect(self.addColboxToTableView_3)
        self.listenToWeb.start()
        
    def addColboxToTableView(self,rowPosition):
        combobox = QtWidgets.QComboBox()
#         combobox.addItem(u'抓取文本')
#         combobox.addItem(u'抓取这个元素的innerHtml')
#         combobox.addItem(u'抓取这个元素的outterHtml')
#         combobox.addItem(u'抓取超链接')
        combobox.addItem(u'不保存')
        combobox.addItem(u'按标题保存')
        combobox.addItem(u'按时间保存')
        combobox.addItem(u'按正文保存')
        
        combobox.row = int(rowPosition)
        combobox.column = 3
        
        self.tableWidget.setCellWidget(int(rowPosition),3,combobox)
        self.addMoreItemToTableWidget()
        
    def addColboxToTableView_2(self,listRow):
        combobox = QtWidgets.QComboBox()
#         combobox.addItem(u'抓取文本')
#         combobox.addItem(u'抓取这个元素的innerHtml')
#         combobox.addItem(u'抓取这个元素的outterHtml')
#         combobox.addItem(u'抓取超链接')
        combobox.addItem(u'元素')
        combobox.addItem(u'输入')
        combobox.addItem(u'单击')
        combobox.addItem(u'获取验证码')
        combobox.addItem(u'输入验证码')
        rowXpath =  listRow[2]
        if rowXpath:
            if rowXpath==u'input':
                combobox.setCurrentIndex(1)
            elif rowXpath==u'a':
                combobox.setCurrentIndex(2)
            elif rowXpath==u'button':
                combobox.setCurrentIndex(2)
            elif rowXpath==u'img':
                combobox.setCurrentIndex(3)
        
        combobox.row = listRow[0]
        combobox.column = listRow[1]
        
        self.tableWidget.setCellWidget(listRow[0],listRow[1],combobox)
        row_num = listRow[0]
        while row_num:
            try:
                if (self.tableWidget.cellWidget(row_num,0).currentText()):
                    row_num = row_num - 1 
                    continue
            except Exception as e:
                break
        if (self.tableWidget.item(row_num,1).text())==u'翻页':
            newItem = QTableWidgetItem(str(0))
            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            self.tableWidget.setItem(listRow[0],7,newItem)
             
            newItem = QTableWidgetItem(str(0))
            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            self.tableWidget.setItem(listRow[0],8,newItem)
            
            self.pageSetDialog = PageSetDialog(self,listRow[0])
            self.pageSetDialog.show()
    
    def addColboxToTableView_3(self,rowPosition,temWebData,scrollYes):
        newItem = QTableWidgetItem(temWebData.get('elementXPath',u''))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,1,newItem)
         
        newItem = QTableWidgetItem(temWebData.get('elementValue',u''))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,2,newItem)
        
        newItem = QTableWidgetItem(temWebData.get('elementId',u''))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,4,newItem)
        
        newItem = QTableWidgetItem(temWebData.get('elementClass',u''))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,5,newItem)
        
        newItem = QTableWidgetItem(temWebData.get('elementInput',u''))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.tableWidget.setItem(rowPosition,6,newItem)
        
        if scrollYes:
            self.tableWidget.setFocus()
            self.tableWidget.selectRow(rowPosition)
            self.tableWidget.scrollToItem(self.tableWidget.item(rowPosition, 1), QAbstractItemView.PositionAtCenter)
            
        
    def showLoadingGif(self):
        self.labels = QtWidgets.QLabel('', self)
        self.labels.setGeometry(self.width()/2,self.height()/2,130,130)
        self.labels.setStyleSheet(("background-color: rgb(255,255,255,0.2);"))
#         self.labels.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);"))
        self.movie = QtGui.QMovie(r":/image/images/1.gif",QByteArray(),self.labels)
        self.labels.setMovie(self.movie)
        
    def showContextMenu(self,pos):
        row_num_list = list(index.row() for index in self.tableWidget.selectedIndexes())
        if len(row_num_list):
            row_num = row_num_list[0]
            row_num_list = set(row_num_list)
            row_num_list = list(row_num_list)
            row_num_list.sort()
            row_num_list.reverse()
            menu = QMenu()
            item1 = menu.addAction(u"删除")
            item2 = menu.addAction(u"查看｜修改")
            item3 = menu.addAction(u"起止页修改")
            action = menu.exec_(self.tableWidget.mapToGlobal(pos))
            if action == item1:
                ok = QMessageBox.question(self, u'删除', u'要删除我？',QMessageBox.Yes,QMessageBox.No)
                if ok== QMessageBox.Yes:
                    for remove_index in row_num_list:
                        self.tableWidget.removeRow(remove_index)
                    for row in range(self.tableWidget.rowCount()):
                        if row >= row_num_list[len(row_num_list)-1]:
                            self.tableWidget.cellWidget(row,0).row = row
                        
            if action == item2:
                try:
                    if (self.tableWidget.cellWidget(row_num_list[0],0).currentText()):
                        self.modifyXpathDialog =  ModifyXpathDialog(self,modify_index=row_num_list[0])
                        self.modifyXpathDialog.show()
                except Exception as e:
                    pass
#                     取消环节上的翻页设置
#                     if (self.tableWidget.item(row_num_list[0],1).text())==u'翻页':
#                         pagNumber = int(self.tableWidget.item(row_num_list[0],4).text())
#                         intNum,ok2 = QInputDialog.getInt(self, u"设置翻页",u"翻页:", pagNumber, 0, 100000)
#                         newItem = QTableWidgetItem(str(intNum))
#                         newItem.setBackground(QtWidgets.QColor(0,255,0))
#                         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#                         self.tableWidget.setItem(row_num_list[0],4,newItem)
            if action == item3:
                try:
                    if (self.tableWidget.item(row_num_list[0],7).text() if self.tableWidget.item(row_num_list[0],7) else ''):
                        start = int(self.tableWidget.item(row_num_list[0],7).text() if self.tableWidget.item(row_num_list[0],7) else '1')
                        end = int(self.tableWidget.item(row_num_list[0],8).text() if self.tableWidget.item(row_num_list[0],8) else '1')
                        
                        self.pageSetDialog = PageSetDialog(self,row_num_list[0],start=start,end=end)
                        self.pageSetDialog.show()
                except Exception as e:
                    pass
#                     取消环节上的翻页设置
#                     if (self.tableWidget.item(row_num_list[0],1).text())==u'翻页':
#                         pagNumber = int(self.tableWidget.item(row_num_list[0],4).text())
#                         intNum,ok2 = QInputDialog.getInt(self, u"设置翻页",u"翻页:", pagNumber, 0, 100000)
#                         newItem = QTableWidgetItem(str(intNum))
#                         newItem.setBackground(QtWidgets.QColor(0,255,0))
#                         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#                         self.tableWidget.setItem(row_num_list[0],4,newItem)
            
                
    def closeTab (self, currentIndex):
        ''' 
        为tab绑定关闭信号，下标为0，不能关闭，备用
        '''
        currentQWidget = self.tabWidget.widget(currentIndex)
        if currentIndex==0:
            ok = QMessageBox.question(self, u'关闭', u'要关闭当前页面吗？',QMessageBox.Yes,QMessageBox.No)
            if ok== QMessageBox.Yes:
                for row in range(self.tableWidget.rowCount()):
                    self.tableWidget.removeRow(0)
                self.bananaIndex = 1
                self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", u"任务:创建任务", None))
                
                now_index =  self.stackedWidget.currentIndex() - 1
                self.stackedWidget.setCurrentIndex(now_index)
                self.lineEdit.setText('')
                self.lineEdit_2.setText('')
                self.currentTaskName = None
            return
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", u"任务:创建任务", None))
        self.tabWidget.setTabEnabled(currentIndex,False)
#         currentQWidget.deleteLater()
#         self.tabWidget.removeTab(currentIndex)

    def rightClickTree(self,pos):
        if self.configId > -1:
            return;
        menu = QMenu()
        item1 = menu.addAction(u"添加主题") 
        item2 = menu.addAction(u"添加类别")
        action = menu.exec_(self.treeWidget.mapToGlobal(pos))
        if action == item1:
            text, ok = QtWidgets.QInputDialog.getText(self, u'添加',
            u'请输入添加的主题:')
            if ok and text:
                addThemeText = '&'.join([str(text),'0'])
                conn = sqlite3.connect(self.dbpath)
                c = conn.cursor()
                # iterate through the records
                c.execute(InitTable.add_new_theme,((addThemeText),self.username,self.configId))
                conn.commit()
                conn.close()
                QMessageBox.information(self, u'提示', u'添加主题成功')
                self.re_inint_tree(needFlush=True)
            else:
                QMessageBox.information(self, u'提示', u'添加主题失败')
        if action == item2:
            addCoffeeDialog = AddCoffeeDialog(self)
            addCoffeeDialog.show()
            addCoffeeDialog.exec_()
            self.re_inint_tree(needFlush=True)
            
    def init_tree(self):
        '''
        初始化数据树,同时初始化comboBox下拉菜单
        '''
#         self.tabWidget.setTabEnabled(1,False)
        
        initParentId = 0
        if self.configId==-1:
            initParentId = -1
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        my_theme = c.execute(InitTable.get_local_theme,(self.configId,self.username,))
        theme_index = 0
        my_theme_store = [theme for theme in my_theme]
#         self.username = my_theme_store[0][2]
        #清空树、下拉菜单
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(3)
        self.treeWidget.hideColumn(1)
        self.treeWidget.hideColumn(2)
        self.comboBox.clear()
        self.comboBox_2.clear()
        for itheme in my_theme_store:
            itheme_split = itheme[1].split('&')
            self.comboBox.addItem(itheme_split[0],itheme_split[1])
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item_0.setText(0,(itheme_split[0]))
            item_0.setText(1,(itheme_split[1]))
            item_0.setFlags(item_0.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

            
            my_coffee = c.execute(InitTable.get_local_coffee,(self.configId,itheme[1],itheme[2],initParentId))
            my_coffee_store = [coffee for coffee in my_coffee]
            
            for icoffee in my_coffee_store:
                icoffee_split = icoffee[1].split('&')
                item_1 = QtWidgets.QTreeWidgetItem(item_0)
                item_1.setText(0, (icoffee_split[0]))
                item_1.setText(1, (icoffee_split[1]))
                item_1.setFlags(item_1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                
                my_task = c.execute(InitTable.get_local_task,(self.configId,icoffee[1],icoffee[2],icoffee[3]))
                my_task_store = [task for task in my_task]
                    
                for itask in my_task_store:
                    item_2 = QtWidgets.QTreeWidgetItem(item_1)
                    item_2.setText(0, _translate("MainWindow", itask[1], None))
                    item_2.setText(2, str(itask[0]))
                    item_2.setFlags(item_2.flags() | Qt.ItemIsUserCheckable)
                    item_2.setCheckState(0, Qt.Unchecked)
                
                #循环处理多级树
                self.initHandleCoffeeTree(itheme,int(icoffee_split[1]),item_1)
            theme_index += 1
        conn.commit()
        conn.close()
        self.treeWidget.itemChanged.connect (self.handleChanged)
        
        self.treeWidget.expandToDepth(1)
        
    def initHandleCoffeeTree(self,itheme,parentCoffeeId,items,addMoreCoffee=False):
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        my_coffee = c.execute(InitTable.get_local_coffee,(self.configId,itheme[1],itheme[2],parentCoffeeId))
        my_coffee_store = [coffee for coffee in my_coffee]
        
        for icoffee in my_coffee_store:
            icoffee_split = icoffee[1].split('&')
            if addMoreCoffee:
                self.comboBox_2.addItem(icoffee_split[0],icoffee_split[1])
            item_1 = QtWidgets.QTreeWidgetItem(items)
            item_1.setText(0, (icoffee_split[0]))
            item_1.setText(1, (icoffee_split[1]))
            item_1.setFlags(item_1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            
            my_task = c.execute(InitTable.get_local_task,(self.configId,icoffee[1],icoffee[2],icoffee[3]))
            my_task_store = [task for task in my_task]
            for itask in my_task_store:
                    item_2 = QtWidgets.QTreeWidgetItem(item_1)
                    item_2.setText(0, _translate("MainWindow", itask[1], None))
                    item_2.setText(2, str(itask[0]))
                    item_2.setFlags(item_2.flags() | Qt.ItemIsUserCheckable)
                    item_2.setCheckState(0, Qt.Unchecked)
            #循环处理多级树
            self.initHandleCoffeeTree(itheme,int(icoffee_split[1]),item_1,addMoreCoffee=addMoreCoffee)
    
    def handleChanged(self, item, column):
        if item.checkState(column) == QtCore.Qt.Checked:
            try:
                self.readyToExport.index(item)
            except Exception as e:
                self.readyToExport.append(item)
        if item.checkState(column) == QtCore.Qt.Unchecked:
            try:
                self.readyToExport.remove(item)
            except Exception as e:
                pass

    def initCurrentUser(self):
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            userInfos = c.execute(InitTable.get_start_user_info)
            for user in userInfos:
                self.username = user[0]
                self.configId = -1
                if user[1]:
                    self.configId = user[1]
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()
        
        #根据configId判断是否需要到远程去更新数据
        if self.configId > 0:
            self.getRemoteConfigInfo()
            #查询对应的configId获取相应的远程配置
            headers={'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
            user_json = {'username':self.username, 'zicada':'2.0'}
            syncByUser = requests.post(self.syncByUserPathStroe,headers=headers,data = json.dumps(user_json))
            syncUserResult = str(syncByUser.content,'utf-8')
            syncByUserData = json.loads(syncUserResult)
            if isinstance(syncByUserData,list):
            #对获取到的流水号和版本进行校验
                sendToRemoteBySerial = self.checkSerialNoAndVersion(syncByUserData)
                if sendToRemoteBySerial:
                    login = requests.post(self.syncBySerialPathStroe,headers=headers,data = json.dumps(sendToRemoteBySerial))
                    needSyncResult = str(login.content,'utf-8')
                    needSyncDatas = json.loads(needSyncResult)
                    if isinstance(needSyncDatas,list) and len(needSyncDatas):
                        self.importDatasToMySqlite3(needSyncDatas)
                        
    def checkSerialNoAndVersion(self,syncByUserData):
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        allSerialAndVerisons = c.execute(InitTable.get_all_serialNum_and_version,(self.configId,self.username,))
        temAllSerialAndVerisons = [[serialAndVersion[0],serialAndVersion[1],serialAndVersion[2]] for serialAndVersion in allSerialAndVerisons]
        tempSerial = [serialAndVersion[1] for serialAndVersion in temAllSerialAndVerisons]
        conn.commit()
        conn.close()
        needSyncSerial = []
        for userData in syncByUserData:
            try:
                serialIndex = tempSerial.index(userData['serialNo'])
                if isinstance(serialIndex,int):
                    serialAndVersion = temAllSerialAndVerisons[serialIndex]
                    #判断版本号是否高于本系统
                    if not serialAndVersion[2] or (isinstance(userData['version'],int) and (userData['version'] > serialAndVersion[2])):
                        needSyncSerial.append({"version":userData['version'],"serialNo":userData['serialNo']})
                        
            except Exception as e:
                needSyncSerial.append({"version":userData['version'],"serialNo":userData['serialNo']})
        
        if len(needSyncSerial):
            return {'username':self.username,'taskInfo':needSyncSerial}
        
    def importDatasToMySqlite3(self,taskJson):
        tempAllThemeNames,tempAllThemeAndCoffeeNames,temAllSerialAndVerisons,tempSerial = self.getThemeAndCoffeeAndTaskAndXpath()
        
        #记录更新的数据
        recodeUpdateData = []
        #记录更新失败的数据
        recodeUpdateFaild = []
        #记录插入的数据
        recodeInsertData = []
        #记录插入失败的数据
        recodeInsertFaild = []
        #未能更新的数据
        recodeCannotUpdate = []
        
        for everyTask in taskJson:
            remoteThemeName = '&'.join([everyTask['themeName'],str(everyTask['themeId'])])
            remoteCoffeeName = '&'.join([everyTask['coffeeName'],str(everyTask['coffeeId'])])
            #判断是否需要插入或更新任务以及数据
            conn = sqlite3.connect(self.dbpath)
            c = conn.cursor()
            try:
                serialIndex = tempSerial.index(everyTask['serialNo'])
                if isinstance(serialIndex,int):
                    serialAndVersion = temAllSerialAndVerisons[serialIndex]
                    #判断版本号是否高于本系统
                    if not serialAndVersion[2] or (isinstance(everyTask['version'],int) and (everyTask['version'] > serialAndVersion[2])):
                        c.execute(InitTable.deleteTaskById,(serialAndVersion[0],))
                        c.execute(InitTable.deleteXpathByTaskId,(serialAndVersion[0],))
#                                     (null,serialName,version,taskName,coffeeName,themeName,username,1,null,taskType
                        c.execute(InitTable.import_insert_new_task_data,(everyTask['serialNo'],everyTask['version'],everyTask['taskName'],remoteCoffeeName,remoteThemeName,self.username,self.configId,))
                        taskId = c.lastrowid
#                                     (null,taskId,taskLink,linkJson,fieldJson,pageJson,1)
                        c.execute(InitTable.insert_new_xpath_data,(taskId,everyTask['xpath']['taskLink'],(json.dumps(everyTask['xpath']['xpathJson'])),))
                        recodeUpdateData.append(everyTask['taskName'])
                    else:
                        recodeCannotUpdate.append(everyTask['taskName'])
                
            except Exception as e:
                c.execute(InitTable.import_insert_new_task_data,(everyTask['serialNo'],everyTask['version'],everyTask['taskName'],remoteCoffeeName,remoteThemeName,self.username,self.configId,))
                taskId = c.lastrowid
#                                     (null,taskId,taskLink,linkJson,fieldJson,pageJson,1)
                c.execute(InitTable.insert_new_xpath_data,(taskId,everyTask['xpath']['taskLink'],(json.dumps(everyTask['xpath']['xpathJson'])),))
                tempSerial.append(everyTask['serialNo'])
                recodeInsertData.append(everyTask['taskName'])
            finally:
                conn.commit()
                conn.close()
             
        return recodeUpdateData,recodeInsertData,recodeCannotUpdate
        
    def getThemeAndCoffeeAndTaskAndXpath(self):
        #先获取所有的主题
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        allThemeNames = c.execute(InitTable.get_all_theme_name,(self.configId,self.username,))
        tempAllThemeNames = [themeName[0] for themeName in allThemeNames]
        
        #获取所有的类别和主题
        allThemeAndCoffeeNames = c.execute(InitTable.get_all_theme_and_coffee_name,(self.configId,self.username,))
        tempAllThemeAndCoffeeNames = [[themeAndCoffeeName[0],themeAndCoffeeName[1]] for themeAndCoffeeName in allThemeAndCoffeeNames]
        
        #获取所有的流水号和版本号
        allSerialAndVerisons = c.execute(InitTable.get_all_serialNum_and_version,(self.configId,self.username,))
        temAllSerialAndVerisons = [[serialAndVersion[0],serialAndVersion[1],serialAndVersion[2]] for serialAndVersion in allSerialAndVerisons]
        tempSerial = [serialAndVersion[1] for serialAndVersion in temAllSerialAndVerisons]
        
        conn.commit()
        conn.close()
        return   tempAllThemeNames,tempAllThemeAndCoffeeNames,temAllSerialAndVerisons,tempSerial
        
    def getRemoteConfigInfo(self):
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            RemoteConfigInfo = c.execute(InitTable.select_config_by_id,(self.configId,))
            currentRemoteConfig = [[info[1],info[2],info[3],info[4],info[5]] for info in RemoteConfigInfo]
            if len(currentRemoteConfig):
                self.systemNameStroe,\
                self.loginPathStroe,\
                self.syncByUserPathStroe,\
                self.syncBySerialPathStroe,\
                self.syncDataPathStroe = currentRemoteConfig[0][0],\
                                        currentRemoteConfig[0][1].encode('utf-8'),\
                                        currentRemoteConfig[0][2].encode('utf-8'),\
                                        currentRemoteConfig[0][3].encode('utf-8'),\
                                        currentRemoteConfig[0][4].encode('utf-8')
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()

    def exportOrSyncDatas(self):
        exportTaskId = []
        storeExportDatasList = []
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            for item in self.readyToExport:
                if item.text(2):
                    task_coffee = item.parent()
                    if task_coffee:
                        task_theme = task_coffee.parent()
                        task_theme = self.getTopTheme(task_theme)
                        if task_theme:
                            exportTaskId.append(int(item.text(2)))
            for nid in exportTaskId:
                needExportData = c.execute(InitTable.get_need_task_and_data,(nid,))
                for da in needExportData:
                    lsDa = list(da)
                    '''
                    t.id,t.serialName,t.version,t.taskName,t.coffeeName,t.themeName,t.username,t.status,t.configId,t.taskType,x.id,x.taskLink,x.linkJson,x.fieldJson,x.pageJson,x.status,x.needSetLogin
                    '''
                    tempExportDatasDict = {'id':lsDa[0],'serialNo':lsDa[1],'version':lsDa[2],'taskName':lsDa[3],'coffeeId':int(lsDa[4].split('&')[1]),'coffeeName':lsDa[4].split('&')[0],'themeId':int(lsDa[5].split('&')[1]),'themeName':lsDa[5].split('&')[0],'username':lsDa[6],'status':lsDa[7],'configId':lsDa[8],'xpath':{'id':lsDa[9],'taskId':lsDa[10],'taskLink':lsDa[11],'xpathJson':json.loads(lsDa[12]),'status':lsDa[13]},'taskType':3}
                    storeExportDatasList.append(tempExportDatasDict)
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()
        return storeExportDatasList
    
    def addMoreItemToTableWidget(self):
        '''
        当列表中有大于等于两条数据时就讲后续的列表自动补齐
        '''
        countItem = self.tableWidget.rowCount()
        if countItem >= 2:
            tableXpath_1 = (self.tableWidget.item(countItem-1,1).text())
            tableXpath_2 = (self.tableWidget.item(countItem-2,1).text())
            if not tableXpath_1 or not tableXpath_2:
                return
            
            selectedFieldIndex = self.tableWidget.cellWidget(countItem-1,0).currentIndex()
            tableXpath_list_1 = tableXpath_1.split('/')
            tableXpath_list_2 = tableXpath_2.split('/')
            
            if len(tableXpath_list_1)==len(tableXpath_list_2):
                for i in range(len(tableXpath_list_1)):
                    if not (tableXpath_list_1[i]==tableXpath_list_2[i]):
                        path_num_str1 =  re.findall(r'\d+',tableXpath_list_1[i])
                        path_num_str2 =  re.findall(r'\d+',tableXpath_list_2[i])
                        if len(path_num_str1) and len(path_num_str2):
                            path_num1 = int(path_num_str1[0])
                            path_num2 = int(path_num_str2[0])
                            increase_num = path_num1
                            if path_num2>path_num1:
                                increase_num = path_num2
                            new_linkXpath_list = tableXpath_list_1
                            increase_num = increase_num+1
                            frame = self.webView.page().currentFrame()
                            selectors = etree.HTML((frame.toHtml()))
                            while increase_num:
                                new_position_str = re.sub('[\d]+',str(increase_num),new_linkXpath_list[i])
                                new_linkXpath_list[i] = new_position_str
                                createdXpath =  '/'.join(new_linkXpath_list)
                                content = selectors.xpath(createdXpath)
                                if len(content):
                                    resultContent =  ''.join(content[0].xpath('string(.)').replace('\n','').split())
                                    
                                    rowPosition = self.tableWidget.rowCount()
                                    self.tableWidget.insertRow(rowPosition)
                                    
                                    combobox_1 = QtWidgets.QComboBox()
                                    combobox_1.addItem(u'元素')
                                    combobox_1.addItem(u'输入')
                                    combobox_1.addItem(u'单击')
                                    combobox_1.addItem(u'获取验证码')
                                    combobox_1.addItem(u'输入验证码')
                                    combobox_1.setCurrentIndex(selectedFieldIndex)
                                    self.tableWidget.setCellWidget(rowPosition,0,combobox_1)
                                    
                                    newItem = QTableWidgetItem((createdXpath))
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,1,newItem)
                                    
                                    newItem = QTableWidgetItem(resultContent)
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,2,newItem)
                                    
                                    
                                    
                                    combobox = QtWidgets.QComboBox()
#                                     combobox.addItem(u'抓取文本')
                                #         combobox.addItem(u'抓取这个元素的innerHtml')
                                #         combobox.addItem(u'抓取这个元素的outterHtml')
#                                     combobox.addItem(u'抓取超链接')
                                    combobox.addItem(u'不保存')
                                    combobox.addItem(u'按标题保存')
                                    combobox.addItem(u'按时间保存')
                                    combobox.addItem(u'按正文保存')
                                    
                                    combobox.row = int(rowPosition)
                                    combobox.column = 3
                                    
                                    self.tableWidget.setCellWidget(int(rowPosition),3,combobox)
                                    
                                    newItem = QTableWidgetItem(u'')
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,4,newItem)
                                    
                                    newItem = QTableWidgetItem(u'')
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,5,newItem)
                                    
                                    newItem = QTableWidgetItem(u'')
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,6,newItem)
                                    
                                else:
                                    break
                                increase_num = increase_num + 1
                        break
                    
    def checkInternetAndReplaceButton33(self):
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
            
        internetUrl = self.lineEdit_2.text()
        internet_addr = (internetUrl)
        if internet_addr.startswith(u'http://') or internet_addr.startswith(u'https://'):
            self.internet_addr = internet_addr
            now_index =  self.stackedWidget.currentIndex() + 1
            self.stackedWidget.setCurrentIndex(now_index)
            self.movie.start()
            if self.labels.isHidden():
                self.labels.setHidden(False)
            #如果任务已经存在，并且链接没有变化，那么就将数据库的数据填充到list中
            
            if self.currentLink and self.currentLink==internet_addr:
                conn = sqlite3.connect(self.dbpath)
                c = conn.cursor()
                try:
                    jsonLinks = c.execute(InitTable.select_task_link_json,(self.currentTaskId,))
                    for links in jsonLinks:
                        linksLoad = json.loads(links[0])
                        for ld in linksLoad:
                            
                            
                            rowPosition = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(rowPosition)
                            
                            newItem = QTableWidgetItem()
                            newItem.setBackground(QtGui.QColor(0,255,0))
                            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                            self.tableWidget.setItem(rowPosition,0,newItem)
                            
                            newItem = QTableWidgetItem(ld['stageName'])
                            newItem.setBackground(QtGui.QColor(0,255,0))
                            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                            self.tableWidget.setItem(rowPosition,1,newItem)
                            
                            newItem = QTableWidgetItem(ld['stageFlag'])
                            newItem.setBackground(QtGui.QColor(0,255,0))
                            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                            self.tableWidget.setItem(rowPosition,2,newItem)
                            
                            self.bananaIndex = ld['stageNo']
                            newItem = QTableWidgetItem(str(self.bananaIndex))
                            newItem.setBackground(QtGui.QColor(0,255,0))
                            newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                            self.tableWidget.setItem(rowPosition,3,newItem)
                            self.bananaIndex += 1
                            
                            
                            currentStageData = ld['stageData']
                            if len(currentStageData):
                                for strawberryData in currentStageData:
                                
                                    rowPosition = self.tableWidget.rowCount()
                                    self.tableWidget.insertRow(rowPosition)
                                    
                                    #原来的没有下拉菜单的情况
#                                     self.tableWidget.setItem(rowPosition,0,QTableWidgetItem(strawberryData['fieldName']))
                                    
                                    #操作xpath的方式
                                    combobox = QtWidgets.QComboBox()
                                    combobox.addItem(u'元素')
                                    combobox.addItem(u'输入')
                                    combobox.addItem(u'单击')
                                    combobox.addItem(u'获取验证码')
                                    combobox.addItem(u'输入验证码')
                                    
                                    combobox.row = int(rowPosition)
                                    combobox.column = 0
                                    
                                    allCoffeeItems = [(combobox.itemText(i)) for i in range(combobox.count())]
                                    idx_coffee = allCoffeeItems.index(strawberryData['fieldName'])
                                    combobox.setCurrentIndex(idx_coffee)
                                    
                                    self.tableWidget.setCellWidget(int(rowPosition),0,combobox)
                                    
                                    newItem = QTableWidgetItem(strawberryData['fieldXpath'])
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,1,newItem)
                                    
                                    newItem = QTableWidgetItem(strawberryData['fieldValue'])
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,2,newItem)
                                    
                                    
                                    #保存方式
                                    combobox = QtWidgets.QComboBox()
#                                     combobox.addItem(u'抓取文本')
                                #         combobox.addItem(u'抓取这个元素的innerHtml')
                                #         combobox.addItem(u'抓取这个元素的outterHtml')
#                                     combobox.addItem(u'抓取超链接')
                                    combobox.addItem(u'不保存')
                                    combobox.addItem(u'按标题保存')
                                    combobox.addItem(u'按时间保存')
                                    combobox.addItem(u'按正文保存')
                                    
                                    combobox.row = int(rowPosition)
                                    combobox.column = 3
                                    
                                    allCoffeeItems = [(combobox.itemText(i)) for i in range(combobox.count())]
                                    idx_coffee = allCoffeeItems.index(strawberryData['fieldType'])
                                    combobox.setCurrentIndex(idx_coffee)
                                    
                                    self.tableWidget.setCellWidget(int(rowPosition),3,combobox)
                                    
                                    newItem = QTableWidgetItem(strawberryData['fieldId'])
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,4,newItem)
                                    
                                    newItem = QTableWidgetItem(strawberryData['fieldClass'])
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,5,newItem)
                                    
                                    newItem = QTableWidgetItem(strawberryData['fieldInput'])
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,6,newItem)
                                    
                                    newItem = QTableWidgetItem(strawberryData['pageNumStart'])
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,7,newItem)
                                    
                                    newItem = QTableWidgetItem(strawberryData['pageNumEnd'])
                                    newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                                    self.tableWidget.setItem(rowPosition,8,newItem)
                            
                except Exception as e:
                    pass
                finally:
                    conn.commit()
                    conn.close()  
            self.webView.load(QUrl(internetUrl))
            
        else:
            QMessageBox.information(self, u'我需要网址', u'请输入正确格式的网址：http://或者https://')
            
    def re_inint_tree(self,needFlush = False):
        initParentId = 0
        if self.configId==-1:
            initParentId = -1
        self.readyToExport.clear()
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        my_theme = c.execute(InitTable.get_local_theme,(self.configId,self.username,))
        theme_index = 0
        my_theme_store = [theme for theme in my_theme]
        self.username = my_theme_store[0][2]
        #清空树、下拉菜单
        self.treeWidget.clear()
        self.treeWidget.setColumnCount(3)
        self.treeWidget.hideColumn(1)
        self.treeWidget.hideColumn(2)
#         self.comboBox.clear()
#         self.comboBox_2.clear()
        if needFlush:
            self.comboBox.clear()
            self.comboBox_2.clear()
        for itheme in my_theme_store:
            itheme_split = itheme[1].split('&')
            if needFlush:
                self.comboBox.addItem(itheme_split[0],itheme_split[1])
#             self.comboBox.addItem(itheme[1])
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item_0.setText(0,(itheme_split[0]))
            item_0.setText(1,(itheme_split[1]))
            item_0.setFlags(item_0.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

            
            my_coffee = c.execute(InitTable.get_local_coffee,(self.configId,itheme[1],itheme[2],initParentId))
            my_coffee_store = [coffee for coffee in my_coffee]
                
            for icoffee in my_coffee_store:
                icoffee_split = icoffee[1].split('&')
                item_1 = QtWidgets.QTreeWidgetItem(item_0)
                item_1.setText(0, (icoffee_split[0]))
                item_1.setText(1, (icoffee_split[1]))
                item_1.setFlags(item_1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                
                my_task = c.execute(InitTable.get_local_task,(self.configId,icoffee[1],icoffee[2],icoffee[3]))
                my_task_store = [task for task in my_task]
                    
                for itask in my_task_store:
                    item_2 = QtWidgets.QTreeWidgetItem(item_1)
                    item_2.setText(0, _translate("MainWindow", itask[1], None))
                    item_2.setText(2, str(itask[0]))
                    item_2.setFlags(item_2.flags() | Qt.ItemIsUserCheckable)
                    item_2.setCheckState(0, Qt.Unchecked)
                #循环处理多级树
                self.initHandleCoffeeTree(itheme,int(icoffee_split[1]),item_1)
                
        
        conn.commit()
        conn.close()
        
        try:
            for parentTheme in self.treeWidget.findItems(self.currentTaskTheme.split('&')[0], QtCore.Qt.MatchFixedString):
                parentTheme.setExpanded(True)
                for indexCoffee in range( parentTheme.childCount()):
                    parentTheme.child(indexCoffee).setExpanded(True)
        except Exception as e:
            self.treeWidget.expandToDepth(1)
        
        self.treeWidget.itemChanged.connect (self.handleChanged)
        
    def saveAllDataToSqlite(self):
        
        internetAddr = (self.lineEdit_2.text())
        
#         ListWidgetData = [{'value':(self.listWidget.item(i).text()),'xpath':(self.listWidget.item(i).data(1))} for i in range(self.listWidget.count())]
#         linkJson = json.dumps(ListWidgetData)
        
        rows = self.tableWidget.rowCount()
        have_get = False
        have_input = False
        for user_index in  range(rows):
            try:
                if (self.tableWidget.cellWidget(user_index,0).currentText())==u'输入验证码':
                    have_input = True
                
                if (self.tableWidget.cellWidget(user_index,0).currentText())==u'获取验证码':
                    have_get = True
            except Exception as e:
                pass
        
        if have_get:
            if have_input:
                pass
            else:
                QMessageBox.information(self, u'提示', u'获取验证码与输入验证码未配对！')
                return
        
        tableWidgetData = []
        yangTaoIndex = 0
        for row_index in range(rows):
            try:
                if not (self.tableWidget.item(row_index,0).text()):
                    yangTaoDict = {'stageName':(self.tableWidget.item(row_index,1).text()),\
                              'stageFlag':(self.tableWidget.item(row_index,2).text()),\
                              'stageNo':int(self.tableWidget.item(row_index,3).text()),\
                              'stageData':[]}
                        
                    tableWidgetData.append(yangTaoDict)
                    yangTaoIndex += 1
                    continue
            except Exception as e:
                tableWidgetDic = {'fieldName':(self.tableWidget.cellWidget(row_index,0).currentText()),\
                                  'fieldXpath':(self.tableWidget.item(row_index,1).text() if self.tableWidget.item(row_index,1) else ''),\
                                  'fieldValue':(self.tableWidget.item(row_index,2).text() if self.tableWidget.item(row_index,2) else ''),\
                                  'fieldType':(self.tableWidget.cellWidget(row_index,3).currentText()),\
                                  'fieldId':(self.tableWidget.item(row_index,4).text() if self.tableWidget.item(row_index,4) else ''),\
                                  'fieldClass':(self.tableWidget.item(row_index,5).text() if self.tableWidget.item(row_index,5) else ''),\
                                  'fieldInput':(self.tableWidget.item(row_index,6).text() if self.tableWidget.item(row_index,6) else ''),\
                                  'pageNumStart':(self.tableWidget.item(row_index,7).text() if self.tableWidget.item(row_index,7) else ''),\
                                  'pageNumEnd':(self.tableWidget.item(row_index,8).text() if self.tableWidget.item(row_index,8) else '')}
                if yangTaoIndex==0:
                    QMessageBox.information(self, u'提示', u'未添加人工干预阶段')
                    return
                tableWidgetData[yangTaoIndex-1]['stageData'].append(tableWidgetDic)
            
        xpathJson = json.dumps(tableWidgetData)
        
        
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        #获取本任务的版本
        my_versions = c.execute(InitTable.get_local_version,(self.currentTaskId,))
        vers = [ver[0] for ver in my_versions]
        version = 1
        if len(vers) and vers[0]:
            version = vers[0] + 1
        conn.commit()
        conn.close()
        #更新任务版本
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            c.execute(InitTable.update_local_version,(version,self.currentTaskId,))
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()
            
        #原数据失效设置
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            c.execute(InitTable.update_local_xpath,(self.currentTaskId,))
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()
            
        #插入新的xpath数据
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            c.execute(InitTable.insert_new_xpath_data,(self.currentTaskId,internetAddr,xpathJson,))
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()
        
        QMessageBox.information(self, u'提示', u'保存成功')
        now_index =  self.stackedWidget.currentIndex() - 1
        self.stackedWidget.setCurrentIndex(now_index)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.currentTaskName = None

class MovieSplashScreen(QtWidgets.QSplashScreen):

    def __init__(self, movie, parent = None):
    
        movie.jumpToFrame(0)
        pixmap = QtGui.QPixmap(movie.frameRect().size())
        
        QtWidgets.QSplashScreen.__init__(self, pixmap)
        self.movie = movie
        self.movie.frameChanged.connect(self.repaint)
    
    def showEvent(self, event):
        self.movie.start()
    
    def hideEvent(self, event):
        self.movie.stop()
    
    def paintEvent(self, event):
    
        painter = QtGui.QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)
    
    def sizeHint(self):
    
        return self.movie.scaledSize()

    
def configSystem():
    app = QtWidgets.QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_():
        movie = QtGui.QMovie(":/image/images/hadppy_newyear.gif")
        splash = MovieSplashScreen(movie)
        splash.show()
        
        start = time.time()
        while movie.state() == QtGui.QMovie.Running and time.time() < start + 4:
            app.processEvents()
        splash.close()
        ui = MainWindow()
        ui.show()
        os._exit(app.exec_())