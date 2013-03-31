# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_ui.ui'
#
# Created: Sun Mar 31 10:33:01 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_publish_form(object):
    def setupUi(self, publish_form):
        publish_form.setObjectName("publish_form")
        publish_form.resize(500, 509)
        publish_form.setAutoFillBackground(False)
        self.verticalLayout_2 = QtGui.QVBoxLayout(publish_form)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.publish_details = QtGui.QLabel(publish_form)
        self.publish_details.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.publish_details.setMargin(30)
        self.publish_details.setObjectName("publish_details")
        self.verticalLayout.addWidget(self.publish_details)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(7)
        self.horizontalLayout_2.setContentsMargins(7, 7, 7, 7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.select_random_btn = QtGui.QPushButton(publish_form)
        self.select_random_btn.setObjectName("select_random_btn")
        self.horizontalLayout_2.addWidget(self.select_random_btn)
        self.select_req_only_btn = QtGui.QPushButton(publish_form)
        self.select_req_only_btn.setObjectName("select_req_only_btn")
        self.horizontalLayout_2.addWidget(self.select_req_only_btn)
        self.select_all_btn = QtGui.QPushButton(publish_form)
        self.select_all_btn.setObjectName("select_all_btn")
        self.horizontalLayout_2.addWidget(self.select_all_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.status_frame = QtGui.QFrame(publish_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_frame.sizePolicy().hasHeightForWidth())
        self.status_frame.setSizePolicy(sizePolicy)
        self.status_frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.status_frame.setStyleSheet("")
        self.status_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.status_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.status_frame.setObjectName("status_frame")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.status_frame)
        self.horizontalLayout_3.setSpacing(7)
        self.horizontalLayout_3.setContentsMargins(7, 7, 7, 7)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.cancel_btn = QtGui.QPushButton(self.status_frame)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_3.addWidget(self.cancel_btn)
        self.publish_btn = QtGui.QPushButton(self.status_frame)
        self.publish_btn.setObjectName("publish_btn")
        self.horizontalLayout_3.addWidget(self.publish_btn)
        self.verticalLayout_2.addWidget(self.status_frame)

        self.retranslateUi(publish_form)
        QtCore.QMetaObject.connectSlotsByName(publish_form)

    def retranslateUi(self, publish_form):
        publish_form.setWindowTitle(QtGui.QApplication.translate("publish_form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.publish_details.setText(QtGui.QApplication.translate("publish_form", "<head/><body><p>Publish details...</p><p><html>", None, QtGui.QApplication.UnicodeUTF8))
        self.select_random_btn.setText(QtGui.QApplication.translate("publish_form", "[randomize_selection]", None, QtGui.QApplication.UnicodeUTF8))
        self.select_req_only_btn.setText(QtGui.QApplication.translate("publish_form", "[select_required_only]", None, QtGui.QApplication.UnicodeUTF8))
        self.select_all_btn.setText(QtGui.QApplication.translate("publish_form", "[select_all]", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_btn.setText(QtGui.QApplication.translate("publish_form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.publish_btn.setText(QtGui.QApplication.translate("publish_form", "Publish", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
