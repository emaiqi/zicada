# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5 import  QtGui,QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

from login.Ui_login import Ui_Dialog
from utils.table_init import InitTable

import utils.auto_test3_image_rc
import base64
import sys,sqlite3,json,requests,types

class LoginDialog(QDialog, Ui_Dialog):
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
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.dbpath = InitTable.dbpath
        self.createUsertable()
        self.isLocal = 1
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.isLocal:
            self.localPasswordLogin()
#             self.accept()
        else:
            self.remotePasswordLogin()
#             self.close()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
        
    @pyqtSlot()
    def on_radioButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.isLocal = 1
    
    @pyqtSlot()
    def on_radioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.isLocal = 0
    
    def createUsertable(self):
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        # create zm_user tables
        try:
            c.execute(InitTable.zm_user)
            # save the changes
            conn.commit()
            c.execute(InitTable.zm_user_insert)
        except sqlite3.OperationalError as o:
            pass
        finally:
            conn.commit()
            # close the connection with the database
            conn.close()
    
    def localPasswordLogin(self):
        '''
        本地登录的账号和密码进行验证，验证成功的话就初始化数据库，否则，让用户重新登录。
        '''
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username and password:
            conn = sqlite3.connect(self.dbpath)
            c = conn.cursor()
            users = c.execute(InitTable.select_local_user)
            for row in users:
                self.user=row
            pass
            conn.commit()
            conn.close()
            if username==self.user[0]:
                if password==self.user[1]:
                    conn = sqlite3.connect(self.dbpath)
                    c = conn.cursor()
                    try:
                        c.execute(InitTable.set_local_user_active)
                        c.execute(InitTable.set_other_user_forbidden)
                    except Exception as e:
                        pass
                    finally:
                        conn.commit()
                        # close the connection with the database
                        conn.close()
                    
                    #初始化数据库
                    self.initDatabase()
                    self.accept()
                else:
                    QtWidgets.QMessageBox.critical(self, 'Error', 'Password error')
            else:
                QtWidgets.QMessageBox.critical(self, 'Error', 'Username error')
        else:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Username or password not null')


    def initDatabase(self):
        '''
        创建默认的配置表、主题表、类别表、任务表、数据表，并初始化本地用户的默认的主题、类别
        '''
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        # create zm_user tables
        try:
            c.execute(InitTable.zm_config)
            c.execute(InitTable.zm_theme)
            c.execute(InitTable.zm_coffee)
            c.execute(InitTable.zm_task)
            c.execute(InitTable.zm_xpath)
            conn.commit()
            c.execute(InitTable.zm_theme_insert )
            c.execute(InitTable.zm_coffee_insert)
#             c.execute(InitTable.zm_task_insert,(InitTable.serialName,))
            conn.commit()
        except sqlite3.OperationalError as o:
            pass
        finally:
            conn.commit()
            # close the connection with the database
            conn.close()
    
    
    def remotePasswordLogin(self):
        '''
        远程密码登录
        '''
        username = (self.lineEdit.text())
        password = (self.lineEdit_2.text()).encode('utf-8')
        if username and password:
            password = base64.encodestring(password)
            #获取当前config表中状态为1的远程系统
            conn = sqlite3.connect(self.dbpath)
            c = conn.cursor()
            try:
                remoteSystemInfo = c.execute(InitTable.select_remote_status_active)
                remoteSystemId = [info[0] for info in remoteSystemInfo]
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Error', u'远程用户不可用')
                return
            finally:
                conn.commit()
                conn.close()
            if len(remoteSystemId):
            #此处要向远程发送请求，返回结果值
                self.getRemoteConfigInfo(remoteSystemId[0])
                headers={'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                payload = {'username':username,'password':str(password,'utf-8')}
                self.loginPathStroe = str(self.loginPathStroe,'utf-8')
                login = requests.post(self.loginPathStroe,headers=headers,data = json.dumps(payload))
                result = json.loads(str(login.content,'utf-8'))
                if result:
                    #远程验证成功,将用户表中的其他数据全部数据状态全部更新为0，不可用状态
                    conn = sqlite3.connect(self.dbpath)
                    c = conn.cursor()
                    try:
                        c.execute(InitTable.update_user_forbidden_status)
                        #插入一条用户记录
                        c.execute(InitTable.insert_new_user_recorde,((username),(password),remoteSystemId[0]))
                    except Exception as e:
                        pass
                    finally:
                        conn.commit()
                        conn.close()
                    self.initThemeAndCoffee(result,username,remoteSystemId[0])
                    self.accept()
                else:
                    QtWidgets.QMessageBox.critical(self, 'Error', u'远程账号或密码不可用')
            else:
                QtWidgets.QMessageBox.critical(self, 'Error', u'远程用户不可用')
                return
            
        else:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Username or password not null')
            
    def getRemoteConfigInfo(self,remoteSystemId):
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        try:
            RemoteConfigInfo = c.execute(InitTable.select_config_by_id,(remoteSystemId,))
            currentRemoteConfig = [[info[1],info[2],info[3],info[4],info[5]] for info in RemoteConfigInfo]
            if len(currentRemoteConfig):
                self.systemNameStroe,self.loginPathStroe = currentRemoteConfig[0][0],currentRemoteConfig[0][1].encode('utf-8')
        except Exception as e:
            pass
        finally:
            conn.commit()
            conn.close()
            
    def getThemeAndCoffeeAndTaskAndXpath(self,username,configId):
        #先获取所有的主题
        conn = sqlite3.connect(self.dbpath)
        c = conn.cursor()
        allThemeNames = c.execute(InitTable.get_all_theme_name,(configId,username,))
        tempAllThemeNames = [themeName[0] for themeName in allThemeNames]
        
        #获取所有的类别和主题
        allThemeAndCoffeeNames = c.execute(InitTable.get_all_theme_and_coffee_name,(configId,username,))
        tempAllThemeAndCoffeeNames = [[themeAndCoffeeName[0],themeAndCoffeeName[1],themeAndCoffeeName[2]] for themeAndCoffeeName in allThemeAndCoffeeNames]
        
        #获取所有的流水号和版本号
        allSerialAndVerisons = c.execute(InitTable.get_all_serialNum_and_version,(configId,username,))
        temAllSerialAndVerisons = [[serialAndVersion[0],serialAndVersion[1],serialAndVersion[2]] for serialAndVersion in allSerialAndVerisons]
        tempSerial = [serialAndVersion[1] for serialAndVersion in temAllSerialAndVerisons]
        
        conn.commit()
        conn.close()
        return   tempAllThemeNames,tempAllThemeAndCoffeeNames,temAllSerialAndVerisons,tempSerial
    
    def initThemeAndCoffee(self,themeAndCoffeeList,username,configId):
        tempAllThemeNames,tempAllThemeAndCoffeeNames,temAllSerialAndVerisons,tempSerial = self.getThemeAndCoffeeAndTaskAndXpath(username,configId)
        for themeAndCoffeeItem in themeAndCoffeeList:
            remoteThemeName = '&'.join([themeAndCoffeeItem['themeName'],str(themeAndCoffeeItem['themeId'])])
            remoteCoffeeName = '&'.join([themeAndCoffeeItem['coffeeName'],str(themeAndCoffeeItem['coffeeId'])])
            parentCoffeeId = themeAndCoffeeItem['parentCoffeeId']
            #判断是否需要插入主题
            conn = sqlite3.connect(self.dbpath)
            c = conn.cursor()
            try:
                themeIndex = tempAllThemeNames.index(remoteThemeName)
                if isinstance(themeIndex,int):
                    print(u'本主题已经存在',remoteThemeName)
            except Exception as e:
                c.execute(InitTable.import_insert_theme,(remoteThemeName,username,configId))
                tempAllThemeNames.append(remoteThemeName)
            finally:
                conn.commit()
                conn.close()
             
            #判读是否需要插入类别
            checkCoffeeAndTheme = [1 for themeAndCoffee in tempAllThemeAndCoffeeNames if themeAndCoffee[0]==remoteThemeName and themeAndCoffee[1]== remoteCoffeeName and themeAndCoffee[2]==parentCoffeeId]
            if not len(checkCoffeeAndTheme):
                conn = sqlite3.connect(self.dbpath)
                c = conn.cursor()
                c.execute(InitTable.import_insert_coffee,(remoteCoffeeName,remoteThemeName,username,configId,parentCoffeeId,))
                tempAllThemeAndCoffeeNames.append([remoteThemeName,remoteCoffeeName,parentCoffeeId])
                conn.commit()
                conn.close()
                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = LoginDialog()
    ui.show()
    sys.exit(app.exec_())