# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output_item_ui.ui'
#
# Created: Mon Apr  1 14:35:34 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(396, 56)
        Form.setMinimumSize(QtCore.QSize(0, 56))
        Form.setMaximumSize(QtCore.QSize(16777215, 56))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.select_cb = QtGui.QCheckBox(Form)
        self.select_cb.setMinimumSize(QtCore.QSize(0, 0))
        self.select_cb.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.select_cb.setText("")
        self.select_cb.setObjectName("select_cb")
        self.verticalLayout.addWidget(self.select_cb)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.icon_label = QtGui.QLabel(Form)
        self.icon_label.setMinimumSize(QtCore.QSize(40, 40))
        self.icon_label.setMaximumSize(QtCore.QSize(40, 40))
        self.icon_label.setBaseSize(QtCore.QSize(32, 32))
        self.icon_label.setText("")
        self.icon_label.setPixmap(QtGui.QPixmap(":/res/default_output.png"))
        self.icon_label.setScaledContents(False)
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_label.setObjectName("icon_label")
        self.horizontalLayout.addWidget(self.icon_label)
        self.details_label = QtGui.QLabel(Form)
        self.details_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.details_label.setMargin(1)
        self.details_label.setObjectName("details_label")
        self.horizontalLayout.addWidget(self.details_label)
        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.details_label.setText(QtGui.QApplication.translate("Form", "<b>Output Name</b><br>Description...<br>the third line...", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
