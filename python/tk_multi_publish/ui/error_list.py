# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error_list.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from tank.platform.qt import QtCore
for name, cls in QtCore.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls

from tank.platform.qt import QtGui
for name, cls in QtGui.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls


from  . import resources_rc

class Ui_ErrorList(object):
    def setupUi(self, ErrorList):
        if not ErrorList.objectName():
            ErrorList.setObjectName(u"ErrorList")
        ErrorList.resize(400, 158)
        self.horizontalLayout = QHBoxLayout(ErrorList)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(12, 2, 2, 2)
        self.main_frame = QFrame(ErrorList)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setStyleSheet(u"#main_frame {\n"
"border-style: solid;\n"
"border-width: 1;\n"
"border-radius: 2px;\n"
"}")
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.main_frame)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.section_label = QLabel(self.main_frame)
        self.section_label.setObjectName(u"section_label")
        self.section_label.setMinimumSize(QSize(0, 20))
        self.section_label.setStyleSheet(u"#section_label {\n"
"font-size: 10pt\n"
"}")
        self.section_label.setIndent(4)

        self.verticalLayout.addWidget(self.section_label)

        self.line = QFrame(self.main_frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.HLine)

        self.verticalLayout.addWidget(self.line)

        self.item_frame = QFrame(self.main_frame)
        self.item_frame.setObjectName(u"item_frame")
        self.item_frame.setStyleSheet(u"#item_frame {\n"
"border-style: none;\n"
"}")
        self.item_frame.setFrameShape(QFrame.StyledPanel)
        self.item_frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.item_frame)

        self.verticalLayout.setStretch(2, 1)

        self.horizontalLayout.addWidget(self.main_frame)

        self.retranslateUi(ErrorList)

        QMetaObject.connectSlotsByName(ErrorList)
    # setupUi

    def retranslateUi(self, ErrorList):
        ErrorList.setWindowTitle(QCoreApplication.translate("ErrorList", u"Form", None))
        self.section_label.setText(QCoreApplication.translate("ErrorList", u"<b><font color='orange'>Validation checks returned some messages for your attention:</font></b>", None))
    # retranslateUi
