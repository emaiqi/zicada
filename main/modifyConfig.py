# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QDialog,QTableWidgetItem,QRadioButton,QMessageBox,QMenu,QApplication
from PyQt5.QtCore import pyqtSlot,Qt

from main.Ui_modifyConfig import Ui_Dialog
from main.ipConfigModify import IpConfigModifyDialog

import utils.auto_test3_image_rc
from utils.table_init import InitTable
import sqlite3,os

class ModifyDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(":/image/images/z-logo.png"))
        self.dbpath = InitTable.dbpath
        self.initTable()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            if self.oldConfigId==self.currentConfigId:
                pass
            else:
                conn = sqlite3.connect(self.dbpath)
                c = conn.cursor()
                try:
                    c.execute(InitTable.update_remote_status_forbidden)
                    c.execute(InitTable.update_remote_selected_id_active,(self.currentConfigId,))
                except Exception as e:
                    pass
                finally:
                    conn.commit()
                    conn.close()
                ok = QMessageBox.question(self, u'退出', u'远程配置已修改，是否重新登录？',QMessageBox.Yes,QMessageBox.No)
                if ok== QMessageBox.Yes:
                    os._exit(0)
            self.close()
        except Exception as e:
            pass
            QMessageBox.information(self, u'提示', u'系统故障，请返厂修复！')
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
    
    def initTable(self):
        listsHorizontalHeaderItem = [u'id',u'系统名称',u'用户验证',u'下载流水号',u'下载数据',u'上传数据',u'状态']
        self.tableWidget.setColumnCount(len(listsHorizontalHeaderItem))
        
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.tableWidget.customContextMenuRequested.connect(self.showContextMenu)
        
        for index in range(self.tableWidget.columnCount()):
            self.tableWidget.setHorizontalHeaderItem(index, QTableWidgetItem(listsHorizontalHeaderItem[index]))
#         rowPosition = self.tableWidget.rowCount()
#         self.tableWidget.insertRow(rowPosition)
# #         newItem = QTableWidgetItem(ld['fieldValue'])
# #         newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
#         self.tableWidget.setItem(rowPosition,0,QTableWidgetItem('good'))
#         self.tableWidget.setItem(rowPosition,1,QTableWidgetItem('good'))
#         self.tableWidget.setItem(rowPosition,2,QTableWidgetItem('good'))
#         self.tableWidget.setItem(rowPosition,3,QTableWidgetItem('good'))
#         moods = QRadioButton("Happy")
#         self.tableWidget.setCellWidget(rowPosition,4,moods)
#         
#         self.tableWidget.insertRow(rowPosition)
#         self.tableWidget.setItem(rowPosition,0,QTableWidgetItem('morning'))
#         self.tableWidget.setItem(rowPosition,1,QTableWidgetItem('morning'))
#         self.tableWidget.setItem(rowPosition,2,QTableWidgetItem('morning'))
#         self.tableWidget.setItem(rowPosition,3,QTableWidgetItem('morning'))
#         moods = QRadioButton("Happy")
#         moods.setChecked(True) 
#         self.tableWidget.setCellWidget(rowPosition,4,moods)
        
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            allConfigDatas = c.execute(InitTable.select_all_config)
            for conf in allConfigDatas:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                
                newItem = QTableWidgetItem(str(conf[0]))
                newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                self.tableWidget.setItem(rowPosition,0,newItem)
                
                newItem = QTableWidgetItem(conf[1])
                newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                self.tableWidget.setItem(rowPosition,1,newItem)
                
                newItem = QTableWidgetItem(conf[2])
                newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                self.tableWidget.setItem(rowPosition,2,newItem)
                
                newItem = QTableWidgetItem(conf[3])
                newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                self.tableWidget.setItem(rowPosition,3,newItem)
                
                newItem = QTableWidgetItem(conf[4])
                newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                self.tableWidget.setItem(rowPosition,4,newItem)
                
                newItem = QTableWidgetItem(conf[5])
                newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                self.tableWidget.setItem(rowPosition,5,newItem)
                
                moods = QRadioButton("selected")
                moods.clicked.connect(self.radioClicked)
                moods.row = rowPosition
                if conf[6]:
                    moods.setChecked(True)
                    self.currentConfigId = self.oldConfigId = conf[0]
                self.tableWidget.setCellWidget(rowPosition,6,moods)
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()
            
    def radioClicked(self):
        radio = self.tableWidget.sender()
        self.currentConfigId = int(self.tableWidget.item(radio.row,0).text())
        
    def showContextMenu(self,pos):
#         print set(index.row() for index in self.tableWidget.selectedIndexes())
        row_num_list = list(index.row() for index in self.tableWidget.selectedIndexes())
        if len(row_num_list):
            row_index = row_num_list[0]
            menu = QMenu()
            item1 = menu.addAction(u"修改")
            action = menu.exec_(self.tableWidget.mapToGlobal(pos))
            if action == item1:
                configId = int((self.tableWidget.item(row_index,0).text()))
                self.icm = IpConfigModifyDialog(configId = configId)
                self.icm.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ModifyDialog()
    ui.show()
    sys.exit(app.exec_())
