# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtWidgets import QDialog,QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

from main.Ui_pageSet import Ui_Dialog

class PageSetDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, pa, rowNum ,start=1,end=2,parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.pa = pa
        self.rowNum = rowNum
        self.spinBox.setValue(start)
        self.spinBox_2.setValue(end)
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        设置起止页码
        """
        newItem = QTableWidgetItem(str(self.spinBox.value()))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.pa.tableWidget.setItem(self.rowNum,7,newItem)
        
        newItem = QTableWidgetItem(str(self.spinBox_2.value()))
        newItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.pa.tableWidget.setItem(self.rowNum,8,newItem)
        
        self.close()
