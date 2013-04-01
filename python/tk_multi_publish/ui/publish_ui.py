# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_ui.ui'
#
# Created: Mon Apr  1 19:08:00 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_publish_form(object):
    def setupUi(self, publish_form):
        publish_form.setObjectName("publish_form")
        publish_form.resize(794, 549)
        publish_form.setAutoFillBackground(False)
        self.verticalLayout = QtGui.QVBoxLayout(publish_form)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.primary_icon_label = QtGui.QLabel(publish_form)
        self.primary_icon_label.setMinimumSize(QtCore.QSize(80, 80))
        self.primary_icon_label.setMaximumSize(QtCore.QSize(80, 80))
        self.primary_icon_label.setBaseSize(QtCore.QSize(32, 32))
        self.primary_icon_label.setText("")
        self.primary_icon_label.setPixmap(QtGui.QPixmap(":/res/default_header.png"))
        self.primary_icon_label.setScaledContents(False)
        self.primary_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.primary_icon_label.setObjectName("primary_icon_label")
        self.horizontalLayout_2.addWidget(self.primary_icon_label)
        self.primary_details_label = QtGui.QLabel(publish_form)
        self.primary_details_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.primary_details_label.setMargin(1)
        self.primary_details_label.setObjectName("primary_details_label")
        self.horizontalLayout_2.addWidget(self.primary_details_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pages = QtGui.QStackedWidget(publish_form)
        self.pages.setObjectName("pages")
        self.publish = QtGui.QWidget()
        self.publish.setObjectName("publish")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.publish)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.publish_details = PublishDetailsWidget(self.publish)
        self.publish_details.setObjectName("publish_details")
        self.horizontalLayout_3.addWidget(self.publish_details)
        self.pages.addWidget(self.publish)
        self.result = QtGui.QWidget()
        self.result.setObjectName("result")
        self.horizontalLayout = QtGui.QHBoxLayout(self.result)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.publish_result = PublishResultWidget(self.result)
        self.publish_result.setObjectName("publish_result")
        self.horizontalLayout.addWidget(self.publish_result)
        self.pages.addWidget(self.result)
        self.verticalLayout.addWidget(self.pages)

        self.retranslateUi(publish_form)
        self.pages.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(publish_form)

    def retranslateUi(self, publish_form):
        publish_form.setWindowTitle(QtGui.QApplication.translate("publish_form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.primary_details_label.setText(QtGui.QApplication.translate("publish_form", "<b>Output Name</b><br>Description...<br>the third line...", None, QtGui.QApplication.UnicodeUTF8))

from ..publish_details_widget import PublishDetailsWidget
from ..publish_result_widget import PublishResultWidget
from . import resources_rc
