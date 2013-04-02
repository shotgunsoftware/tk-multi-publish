# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_form.ui'
#
# Created: Tue Apr  2 18:23:41 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PublishForm(object):
    def setupUi(self, PublishForm):
        PublishForm.setObjectName("PublishForm")
        PublishForm.resize(794, 549)
        PublishForm.setAutoFillBackground(False)
        self.verticalLayout = QtGui.QVBoxLayout(PublishForm)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.primary_icon_label = QtGui.QLabel(PublishForm)
        self.primary_icon_label.setMinimumSize(QtCore.QSize(80, 80))
        self.primary_icon_label.setMaximumSize(QtCore.QSize(80, 80))
        self.primary_icon_label.setBaseSize(QtCore.QSize(32, 32))
        self.primary_icon_label.setText("")
        self.primary_icon_label.setPixmap(QtGui.QPixmap(":/res/default_header.png"))
        self.primary_icon_label.setScaledContents(False)
        self.primary_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.primary_icon_label.setObjectName("primary_icon_label")
        self.horizontalLayout_2.addWidget(self.primary_icon_label)
        self.primary_details_label = QtGui.QLabel(PublishForm)
        self.primary_details_label.setStyleSheet("#primary_details_label {\n"
"font-size: 16pt;\n"
"}")
        self.primary_details_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.primary_details_label.setMargin(1)
        self.primary_details_label.setObjectName("primary_details_label")
        self.horizontalLayout_2.addWidget(self.primary_details_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pages = QtGui.QStackedWidget(PublishForm)
        self.pages.setObjectName("pages")
        self.publish_details = PublishDetailsForm()
        self.publish_details.setObjectName("publish_details")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.publish_details)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pages.addWidget(self.publish_details)
        self.publish_result = PublishResultForm()
        self.publish_result.setObjectName("publish_result")
        self.horizontalLayout = QtGui.QHBoxLayout(self.publish_result)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pages.addWidget(self.publish_result)
        self.verticalLayout.addWidget(self.pages)

        self.retranslateUi(PublishForm)
        self.pages.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(PublishForm)

    def retranslateUi(self, PublishForm):
        PublishForm.setWindowTitle(QtGui.QApplication.translate("PublishForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.primary_details_label.setText(QtGui.QApplication.translate("PublishForm", "<b>Output Name</b><br>Description...<br>the third line...", None, QtGui.QApplication.UnicodeUTF8))

from ..publish_result_form import PublishResultForm
from ..publish_details_form import PublishDetailsForm
from . import resources_rc
