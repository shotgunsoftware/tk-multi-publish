# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_ui.ui'
#
# Created: Mon Apr  1 14:35:34 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_publish_form(object):
    def setupUi(self, publish_form):
        publish_form.setObjectName("publish_form")
        publish_form.resize(560, 485)
        publish_form.setAutoFillBackground(False)
        self.verticalLayout_2 = QtGui.QVBoxLayout(publish_form)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.primary_icon_label_2 = QtGui.QLabel(publish_form)
        self.primary_icon_label_2.setMinimumSize(QtCore.QSize(80, 80))
        self.primary_icon_label_2.setMaximumSize(QtCore.QSize(80, 80))
        self.primary_icon_label_2.setBaseSize(QtCore.QSize(32, 32))
        self.primary_icon_label_2.setText("")
        self.primary_icon_label_2.setPixmap(QtGui.QPixmap(":/res/default_header.png"))
        self.primary_icon_label_2.setScaledContents(False)
        self.primary_icon_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.primary_icon_label_2.setObjectName("primary_icon_label_2")
        self.horizontalLayout_2.addWidget(self.primary_icon_label_2)
        self.primary_details_label_2 = QtGui.QLabel(publish_form)
        self.primary_details_label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.primary_details_label_2.setMargin(1)
        self.primary_details_label_2.setObjectName("primary_details_label_2")
        self.horizontalLayout_2.addWidget(self.primary_details_label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.main_widget_area = QtGui.QStackedWidget(publish_form)
        self.main_widget_area.setObjectName("main_widget_area")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.main_widget_area.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")
        self.main_widget_area.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.main_widget_area)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(publish_form)
        QtCore.QMetaObject.connectSlotsByName(publish_form)

    def retranslateUi(self, publish_form):
        publish_form.setWindowTitle(QtGui.QApplication.translate("publish_form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.primary_details_label_2.setText(QtGui.QApplication.translate("publish_form", "<b>Output Name</b><br>Description...<br>the third line...", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
from . import resources_rc
