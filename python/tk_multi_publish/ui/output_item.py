# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'output_item.ui'
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

class Ui_OutputItem(object):
    def setupUi(self, OutputItem):
        if not OutputItem.objectName():
            OutputItem.setObjectName(u"OutputItem")
        OutputItem.resize(396, 56)
        OutputItem.setMinimumSize(QSize(0, 56))
        OutputItem.setMaximumSize(QSize(16777215, 56))
        self.horizontalLayout = QHBoxLayout(OutputItem)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(12, 2, 2, 2)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.select_cb = QCheckBox(OutputItem)
        self.select_cb.setObjectName(u"select_cb")
        self.select_cb.setMinimumSize(QSize(0, 0))
        self.select_cb.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.select_cb)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.icon_label = QLabel(OutputItem)
        self.icon_label.setObjectName(u"icon_label")
        self.icon_label.setMinimumSize(QSize(40, 40))
        self.icon_label.setMaximumSize(QSize(40, 40))
        self.icon_label.setBaseSize(QSize(32, 32))
        self.icon_label.setPixmap(QPixmap(u":/res/default_output.png"))
        self.icon_label.setScaledContents(False)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setIndent(0)

        self.horizontalLayout.addWidget(self.icon_label)

        self.details_label = QLabel(OutputItem)
        self.details_label.setObjectName(u"details_label")
        self.details_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.details_label.setMargin(0)
        self.details_label.setIndent(0)

        self.horizontalLayout.addWidget(self.details_label)

        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(OutputItem)

        QMetaObject.connectSlotsByName(OutputItem)
    # setupUi

    def retranslateUi(self, OutputItem):
        OutputItem.setWindowTitle(QCoreApplication.translate("OutputItem", u"Form", None))
        self.select_cb.setText("")
        self.icon_label.setText("")
        self.details_label.setText(QCoreApplication.translate("OutputItem", u"<b>Output Name</b><br>Description...<br>the third line...", None))
    # retranslateUi
