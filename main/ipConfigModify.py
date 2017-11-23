# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5 import  QtGui
from PyQt5.QtWidgets import QDialog,QMessageBox
from PyQt5.QtCore import pyqtSlot

from main.Ui_ipConfig_2 import Ui_Dialog

import utils.auto_test3_image_rc
from utils.table_init import InitTable
import sqlite3,os

class IpConfigModifyDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, configId = 0,parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(":/image/images/z-logo.png"))
        self.dbpath = InitTable.dbpath
        self.configId = configId
        self.initConfigDialog()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        systemName = (self.lineEdit.text())
        ip = (self.lineEdit_2.text())
        port = (self.lineEdit_3.text())
        systemPrefix = (self.lineEdit_4.text())
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        flag = False
        try:
            if systemName and ip and port and systemPrefix:
                systemName = systemName.strip()
                ip = ip.strip()
                port = port.strip()
                systemPrefix = systemPrefix.strip()
                logPath = u'http://{0}:{1}/{2}/dataSyn/checkUserAuthority'.format(ip,port,systemPrefix)
                syncByUserPath = u'http://{0}:{1}/{2}/dataSyn/synDataByUsername'.format(ip,port,systemPrefix)
                syncBySerialPath = u'http://{0}:{1}/{2}/dataSyn/synDataBySerialNo'.format(ip,port,systemPrefix)
                syncDataPath = u'http://{0}:{1}/{2}/dataSyn/synData'.format(ip,port,systemPrefix)
                c.execute(InitTable.update_remote_config,(systemName,logPath,syncByUserPath,syncBySerialPath,syncDataPath,self.configId))
                flag = True
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()
        if flag:
            ok = QMessageBox.question(self, u'退出', u'重新登录后配置生效，是否重新登录？',QMessageBox.Yes,QMessageBox.No)
            if ok== QMessageBox.Yes:
                os._exit(0)
        
        self.close()
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
        
    def initConfigDialog(self):
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            RemoteConfigInfo = c.execute(InitTable.select_config_by_id,(self.configId,))
            currentRemoteConfig = [[info[1],info[2]] for info in RemoteConfigInfo]
            if len(currentRemoteConfig):
                self.lineEdit.setText(currentRemoteConfig[0][0])
                handleConfig = currentRemoteConfig[0][1].split('/')
                self.lineEdit_2.setText(handleConfig[2].split(':')[0])
                self.lineEdit_3.setText(handleConfig[2].split(':')[1])
                self.lineEdit_4.setText(handleConfig[3])
                
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()
        
