# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_item_ui.ui'
#
# Created: Mon Apr  1 19:42:35 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(324, 36)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.error_label = QtGui.QLabel(Form)
        self.error_label.setMinimumSize(QtCore.QSize(0, 0))
        self.error_label.setStyleSheet("")
        self.error_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.error_label.setObjectName("error_label")
        self.horizontalLayout.addWidget(self.error_label)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.error_label.setText(QtGui.QApplication.translate("Form", "<font color=\'orange\'>Validation Name</font><br>Details on how to fix etc.", None, QtGui.QApplication.UnicodeUTF8))

