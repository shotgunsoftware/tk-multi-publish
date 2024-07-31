# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'group_header.ui'
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


class Ui_GroupHeader(object):
    def setupUi(self, GroupHeader):
        if not GroupHeader.objectName():
            GroupHeader.setObjectName(u"GroupHeader")
        GroupHeader.resize(394, 50)
        GroupHeader.setMinimumSize(QSize(0, 50))
        GroupHeader.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(GroupHeader)
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.name_label = QLabel(GroupHeader)
        self.name_label.setObjectName(u"name_label")
        self.name_label.setStyleSheet(u"#name_label {\n"
"font-size: 16px\n"
"}")
        self.name_label.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.name_label)

        self.line = QFrame(GroupHeader)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.HLine)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(GroupHeader)

        QMetaObject.connectSlotsByName(GroupHeader)
    # setupUi

    def retranslateUi(self, GroupHeader):
        GroupHeader.setWindowTitle(QCoreApplication.translate("GroupHeader", u"Form", None))
        self.name_label.setText(QCoreApplication.translate("GroupHeader", u"Group Display Name", None))
    # retranslateUi
