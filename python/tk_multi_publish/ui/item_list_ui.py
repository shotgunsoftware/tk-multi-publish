# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'item_list_ui.ui'
#
# Created: Mon Apr  1 19:42:34 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(397, 265)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.main_frame = QtGui.QFrame(Form)
        self.main_frame.setStyleSheet("#main_frame {\n"
"border-style: solid;\n"
"border-width: 1;\n"
"border-radius: 2px;\n"
"}")
        self.main_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.main_frame)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.section_label = QtGui.QLabel(self.main_frame)
        self.section_label.setStyleSheet("#section_label {\n"
"font-size: 10pt\n"
"}")
        self.section_label.setObjectName("section_label")
        self.horizontalLayout.addWidget(self.section_label)
        self.expand_label = QtGui.QLabel(self.main_frame)
        self.expand_label.setMinimumSize(QtCore.QSize(20, 20))
        self.expand_label.setBaseSize(QtCore.QSize(20, 20))
        self.expand_label.setText("")
        self.expand_label.setPixmap(QtGui.QPixmap(":/res/group_expand.png"))
        self.expand_label.setScaledContents(False)
        self.expand_label.setAlignment(QtCore.Qt.AlignCenter)
        self.expand_label.setObjectName("expand_label")
        self.horizontalLayout.addWidget(self.expand_label)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(self.main_frame)
        self.line.setFrameShadow(QtGui.QFrame.Plain)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.item_frame = QtGui.QFrame(self.main_frame)
        self.item_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.item_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.item_frame.setObjectName("item_frame")
        self.verticalLayout.addWidget(self.item_frame)
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout_2.addWidget(self.main_frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.section_label.setText(QtGui.QApplication.translate("Form", "<b>n items available</b>, <i>expand to turn individual items on and off</i>", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
