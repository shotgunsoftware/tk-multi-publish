# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error_item.ui'
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


class Ui_ErrorItem(object):
    def setupUi(self, ErrorItem):
        if not ErrorItem.objectName():
            ErrorItem.setObjectName(u"ErrorItem")
        ErrorItem.resize(324, 36)
        self.horizontalLayout = QHBoxLayout(ErrorItem)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.error_label = QLabel(ErrorItem)
        self.error_label.setObjectName(u"error_label")
        self.error_label.setMinimumSize(QSize(0, 0))
        self.error_label.setStyleSheet(u"")
        self.error_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout.addWidget(self.error_label)

        self.retranslateUi(ErrorItem)

        QMetaObject.connectSlotsByName(ErrorItem)
    # setupUi

    def retranslateUi(self, ErrorItem):
        ErrorItem.setWindowTitle(QCoreApplication.translate("ErrorItem", u"Form", None))
        self.error_label.setText(QCoreApplication.translate("ErrorItem", u"<font color='orange'>Validation Name</font><br>Details on how to fix etc.", None))
    # retranslateUi
