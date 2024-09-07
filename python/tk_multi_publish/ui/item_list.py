# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item_list.ui'
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

class Ui_ItemList(object):
    def setupUi(self, ItemList):
        if not ItemList.objectName():
            ItemList.setObjectName(u"ItemList")
        ItemList.resize(397, 265)
        self.horizontalLayout_2 = QHBoxLayout(ItemList)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(12, 2, 2, 2)
        self.main_frame = QFrame(ItemList)
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
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.section_label = QLabel(self.main_frame)
        self.section_label.setObjectName(u"section_label")
        self.section_label.setStyleSheet(u"#section_label {\n"
"font-size: 10pt\n"
"}")
        self.section_label.setIndent(4)

        self.horizontalLayout.addWidget(self.section_label)

        self.expand_label = QLabel(self.main_frame)
        self.expand_label.setObjectName(u"expand_label")
        self.expand_label.setMinimumSize(QSize(20, 20))
        self.expand_label.setBaseSize(QSize(20, 20))
        self.expand_label.setPixmap(QPixmap(u":/res/group_expand.png"))
        self.expand_label.setScaledContents(False)
        self.expand_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.expand_label)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

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

        self.horizontalLayout_2.addWidget(self.main_frame)

        self.retranslateUi(ItemList)

        QMetaObject.connectSlotsByName(ItemList)
    # setupUi

    def retranslateUi(self, ItemList):
        ItemList.setWindowTitle(QCoreApplication.translate("ItemList", u"Form", None))
        self.section_label.setText(QCoreApplication.translate("ItemList", u"<b>n items available</b>, <i>expand to turn individual items on and off</i>", None))
        self.expand_label.setText("")
    # retranslateUi
