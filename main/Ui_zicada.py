# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Users\ericforpython\pywork\eric_project_learn\xpath-gather-nine\main.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtWebKitWidgets import QWebView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(("MainWindow"))
        MainWindow.resize(1444, 999)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap((":/image/images/z-logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet((""))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName(("centralWidget"))
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_4.setObjectName(("gridLayout_4"))
        self.treeWidget = QtWidgets.QTreeWidget(self.centralWidget)
        self.treeWidget.setMinimumSize(QtCore.QSize(400, 0))
        self.treeWidget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.treeWidget.setStyleSheet((""))
        self.treeWidget.setObjectName(("treeWidget"))
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        self.gridLayout_4.addWidget(self.treeWidget, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(("tabWidget"))
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName(("tab"))
        self.tabWidget.addTab(self.tab, (""))
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName(("tab_2"))
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(("gridLayout_3"))
        self.stackedWidget = QtWidgets.QStackedWidget(self.tab_2)
        self.stackedWidget.setObjectName(("stackedWidget"))
        self.page = QtWidgets.QWidget()
        self.page.setObjectName(("page"))
        self.gridLayoutWidget = QtWidgets.QWidget(self.page)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 831, 381))
        self.gridLayoutWidget.setObjectName(("gridLayoutWidget"))
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(("gridLayout_2"))
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_2.setObjectName(("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label.setObjectName(("label"))
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 35))
        self.comboBox.setObjectName(("comboBox"))
        self.gridLayout_2.addWidget(self.comboBox, 2, 3, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lineEdit_2.setStyleSheet(("font: 16pt \"Arial\";"))
        self.lineEdit_2.setObjectName(("lineEdit_2"))
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_3.setObjectName(("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 11))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lineEdit.setStyleSheet(("font: 16pt \"Arial\";"))
        self.lineEdit.setText((""))
        self.lineEdit.setObjectName(("lineEdit"))
        self.gridLayout_2.addWidget(self.lineEdit, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_4.setObjectName(("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_2.setMaximumSize(QtCore.QSize(16777215, 35))
        self.comboBox_2.setObjectName(("comboBox_2"))
        self.gridLayout_2.addWidget(self.comboBox_2, 3, 3, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.page)
        self.pushButton_3.setGeometry(QtCore.QRect(690, 410, 141, 41))
        self.pushButton_3.setMaximumSize(QtCore.QSize(16777215, 150))
        self.pushButton_3.setObjectName(("pushButton_3"))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName(("page_2"))
        self.gridLayout = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout.setObjectName(("gridLayout"))
        self.tableWidget = QtWidgets.QTableWidget(self.page_2)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 200))
        self.tableWidget.setObjectName(("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 4, 1, 1, 1)
        self.widget = QtWidgets.QWidget(self.page_2)
        self.widget.setMinimumSize(QtCore.QSize(0, 50))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget.setObjectName(("widget"))
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(10, 0, 150, 50))
        self.pushButton.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton.setObjectName(("pushButton"))
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 0, 150, 50))
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_2.setObjectName(("pushButton_2"))
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(350, 0, 150, 50))
        self.pushButton_4.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_4.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_4.setObjectName(("pushButton_4"))
        self.pushButton_5 = QtWidgets.QPushButton(self.widget)
        self.pushButton_5.setGeometry(QtCore.QRect(520, 0, 150, 50))
        self.pushButton_5.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_5.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_5.setObjectName(("pushButton_5"))
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(720, 10, 71, 31))
        self.doubleSpinBox.setMinimum(0.6)
        self.doubleSpinBox.setMaximum(1.0)
        self.doubleSpinBox.setSingleStep(0.02)
        self.doubleSpinBox.setProperty("value", 1.0)
        self.doubleSpinBox.setObjectName(("doubleSpinBox"))
        self.gridLayout.addWidget(self.widget, 1, 1, 2, 1)
        self.webView = QWebView(self.page_2)
        self.webView.setUrl(QtCore.QUrl(("about:blank")))
        self.webView.setObjectName(("webView"))
        self.gridLayout.addWidget(self.webView, 5, 1, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout_3.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, (""))
        self.gridLayout_4.addWidget(self.tabWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1444, 26))
        self.menuBar.setObjectName(("menuBar"))
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName(("menuFile"))
        self.menuSetting = QtWidgets.QMenu(self.menuBar)
        self.menuSetting.setObjectName(("menuSetting"))
        self.menuAbout = QtWidgets.QMenu(self.menuBar)
        self.menuAbout.setObjectName(("menuAbout"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionUpdate = QtWidgets.QAction(MainWindow)
        self.actionUpdate.setObjectName(("actionUpdate"))
        self.actionSynchronizastion = QtWidgets.QAction(MainWindow)
        self.actionSynchronizastion.setObjectName(("actionSynchronizastion"))
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName(("actionExport"))
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName(("actionImport"))
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName(("actionExit"))
        self.actionConfig_param = QtWidgets.QAction(MainWindow)
        self.actionConfig_param.setObjectName(("actionConfig_param"))
        self.actionModify_config = QtWidgets.QAction(MainWindow)
        self.actionModify_config.setObjectName(("actionModify_config"))
        self.actionModify_local_password = QtWidgets.QAction(MainWindow)
        self.actionModify_local_password.setObjectName(("actionModify_local_password"))
        self.actionShow_all_data = QtWidgets.QAction(MainWindow)
        self.actionShow_all_data.setObjectName(("actionShow_all_data"))
        self.actionInfo = QtWidgets.QAction(MainWindow)
        self.actionInfo.setObjectName(("actionInfo"))
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionSynchronizastion)
#         self.menuFile.addAction(self.actionUpdate)
        self.menuFile.addAction(self.actionExit)
        self.menuSetting.addAction(self.actionConfig_param)
        self.menuSetting.addAction(self.actionModify_config)
#         self.menuSetting.addAction(self.actionModify_local_password)
#         self.menuSetting.addAction(self.actionShow_all_data)
        self.menuAbout.addAction(self.actionInfo)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSetting.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", u"Zicada爬虫脚本录制客户端", None))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "beijing", None))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "tian an men", None))
        self.treeWidget.topLevelItem(0).child(0).child(0).setText(0, _translate("MainWindow", "gugong", None))
        self.treeWidget.topLevelItem(0).child(0).child(1).setText(0, _translate("MainWindow", "tiantan", None))
        self.treeWidget.topLevelItem(0).child(0).child(2).setText(0, _translate("MainWindow", "renmindahuitang", None))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "hebei", None))
        self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "cangzhou", None))
        self.treeWidget.topLevelItem(1).child(0).child(0).setText(0, _translate("MainWindow", "tieshizi", None))
        self.treeWidget.topLevelItem(1).child(0).child(1).setText(0, _translate("MainWindow", "zaji", None))
        self.treeWidget.topLevelItem(1).child(0).child(2).setText(0, _translate("MainWindow", "yunhe", None))
        self.treeWidget.topLevelItem(1).child(1).setText(0, _translate("MainWindow", "qinhuangdao", None))
        self.treeWidget.topLevelItem(1).child(1).child(0).setText(0, _translate("MainWindow", "yanshandaxue", None))
        self.treeWidget.topLevelItem(1).child(1).child(1).setText(0, _translate("MainWindow", "beidaihe", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.label_2.setText(_translate("MainWindow", u"任务名称:", None))
        self.label.setText(_translate("MainWindow", u"链接地址:", None))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", u"请输入链接地址", None))
        self.label_3.setText(_translate("MainWindow", u"主题名称:", None))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", u"请输入任务名称", None))
        self.label_4.setText(_translate("MainWindow", u"类别名称:", None))
        self.pushButton_3.setText(_translate("MainWindow", u"下一步", None))
        self.pushButton.setText(_translate("MainWindow", u"环节设置", None))
        self.pushButton_2.setText(_translate("MainWindow", u"清空列表", None))
        self.pushButton_4.setText(_translate("MainWindow", u"关闭", None))
        self.pushButton_5.setText(_translate("MainWindow", u"完成", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "任务:任务名称", None))
        self.menuFile.setTitle(_translate("MainWindow", u"文件", None))
        self.menuSetting.setTitle(_translate("MainWindow", u"设置", None))
        self.menuAbout.setTitle(_translate("MainWindow", u"关于", None))
        self.actionUpdate.setText(_translate("MainWindow", "update", None))
        self.actionSynchronizastion.setText(_translate("MainWindow", u"同步", None))
        self.actionExport.setText(_translate("MainWindow", u"导出", None))
        self.actionImport.setText(_translate("MainWindow", u"导入", None))
        self.actionExit.setText(_translate("MainWindow", u"退出", None))
        self.actionConfig_param.setText(_translate("MainWindow", u"配置远程参数", None))
        self.actionModify_config.setText(_translate("MainWindow", u"修改远程配置", None))
        self.actionModify_local_password.setText(_translate("MainWindow", "modify local password", None))
        self.actionShow_all_data.setText(_translate("MainWindow", "show all datas", None))
        self.actionInfo.setText(_translate("MainWindow", u"信息", None))

from PyQt5 import QtWebKit
import utils.auto_test3_image_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
