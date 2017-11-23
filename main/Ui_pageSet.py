# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Users\ericforpython\pywork\eric_project_learn\xpath-gather-nine-bak\pageSet.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(("Dialog"))
        Dialog.resize(407, 122)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 61))
        self.horizontalLayoutWidget.setObjectName(("horizontalLayoutWidget"))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(("horizontalLayout"))
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet(("font: 12pt \"Arial\";"))
        self.label.setLocale(QtCore.QLocale(QtCore.QLocale.CongoSwahili, QtCore.QLocale.DemocraticRepublicOfCongo))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(("label"))
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBox.setStyleSheet(("font: 12pt \"Arial\";"))
        self.spinBox.setMaximum(1000000)
        self.spinBox.setObjectName(("spinBox"))
        self.horizontalLayout.addWidget(self.spinBox)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setStyleSheet(("font: 12pt \"Arial\";"))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBox_2.setStyleSheet(("font: 12pt \"Arial\";"))
        self.spinBox_2.setMaximum(1000000)
        self.spinBox_2.setObjectName(("spinBox_2"))
        self.horizontalLayout.addWidget(self.spinBox_2)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(140, 67, 93, 41))
        self.pushButton.setStyleSheet(("font: 12pt \"Arial\";"))
        self.pushButton.setObjectName(("pushButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", u"起止页修改", None))
        self.label.setText(_translate("Dialog", u"从:", None))
        self.label_2.setText(_translate("Dialog", u"到:", None))
        self.pushButton.setText(_translate("Dialog", "ok", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

