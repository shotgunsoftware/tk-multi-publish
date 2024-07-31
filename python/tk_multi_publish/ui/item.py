# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item.ui'
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


class Ui_Item(object):
    def setupUi(self, Item):
        if not Item.objectName():
            Item.setObjectName(u"Item")
        Item.resize(314, 38)
        self.horizontalLayout = QHBoxLayout(Item)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.select_cb = QCheckBox(Item)
        self.select_cb.setObjectName(u"select_cb")
        self.select_cb.setMinimumSize(QSize(0, 0))
        self.select_cb.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.select_cb)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.details_label = QLabel(Item)
        self.details_label.setObjectName(u"details_label")
        self.details_label.setMinimumSize(QSize(0, 0))
        self.details_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.details_label.setMargin(1)

        self.horizontalLayout.addWidget(self.details_label)

        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(Item)

        QMetaObject.connectSlotsByName(Item)
    # setupUi

    def retranslateUi(self, Item):
        Item.setWindowTitle(QCoreApplication.translate("Item", u"Form", None))
        self.select_cb.setText("")
        self.details_label.setText(QCoreApplication.translate("Item", u"<b>Item Name</b><br>Description...", None))
    # retranslateUi
