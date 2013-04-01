# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_details_ui.ui'
#
# Created: Mon Apr  1 14:35:35 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(859, 537)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.items_title_label = QtGui.QLabel(Form)
        self.items_title_label.setStyleSheet("#items_title_label {\n"
"font-size: 16px\n"
"}")
        self.items_title_label.setObjectName("items_title_label")
        self.verticalLayout_7.addWidget(self.items_title_label)
        self.items_scroll = QtGui.QScrollArea(Form)
        self.items_scroll.setStyleSheet("#items_scroll {\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2px;\n"
"border-color: rgb(32,32,32);\n"
"}")
        self.items_scroll.setWidgetResizable(True)
        self.items_scroll.setObjectName("items_scroll")
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 515, 470))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.items_scroll.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_7.addWidget(self.items_scroll)
        self.verticalLayout_7.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.info_title_label = QtGui.QLabel(Form)
        self.info_title_label.setStyleSheet("#info_title_label {\n"
"font-size: 16px\n"
"}")
        self.info_title_label.setObjectName("info_title_label")
        self.verticalLayout_5.addWidget(self.info_title_label)
        self.info_frame = QtGui.QFrame(Form)
        self.info_frame.setStyleSheet("#info_frame {\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2px;\n"
"border-color: rgb(32,32,32);\n"
"}\n"
"QLabel {\n"
"font-size: 14px;\n"
"}")
        self.info_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.info_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.info_frame.setObjectName("info_frame")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.info_frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtGui.QLabel(self.info_frame)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.sg_task_combo = QtGui.QComboBox(self.info_frame)
        self.sg_task_combo.setObjectName("sg_task_combo")
        self.verticalLayout_6.addWidget(self.sg_task_combo)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem)
        self.label_7 = QtGui.QLabel(self.info_frame)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.thumbnail_widget = QtGui.QWidget(self.info_frame)
        self.thumbnail_widget.setMinimumSize(QtCore.QSize(160, 100))
        self.thumbnail_widget.setObjectName("thumbnail_widget")
        self.horizontalLayout_6.addWidget(self.thumbnail_widget)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        spacerItem2 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem2)
        self.label_8 = QtGui.QLabel(self.info_frame)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_6.addWidget(self.label_8)
        self.comments_edit = QtGui.QTextEdit(self.info_frame)
        self.comments_edit.setMinimumSize(QtCore.QSize(300, 0))
        self.comments_edit.setObjectName("comments_edit")
        self.verticalLayout_6.addWidget(self.comments_edit)
        self.verticalLayout_5.addWidget(self.info_frame)
        self.verticalLayout_5.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.status_frame = QtGui.QFrame(Form)
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
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.status_frame)
        self.horizontalLayout_7.setSpacing(7)
        self.horizontalLayout_7.setContentsMargins(7, 7, 7, 7)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.cancel_btn = QtGui.QPushButton(self.status_frame)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_7.addWidget(self.cancel_btn)
        self.publish_btn = QtGui.QPushButton(self.status_frame)
        self.publish_btn.setObjectName("publish_btn")
        self.horizontalLayout_7.addWidget(self.publish_btn)
        self.verticalLayout.addWidget(self.status_frame)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.items_title_label.setText(QtGui.QApplication.translate("Form", "Choose Additional Items to Publish:", None, QtGui.QApplication.UnicodeUTF8))
        self.info_title_label.setText(QtGui.QApplication.translate("Form", "Add Information about your Publish:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "What are you working on?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Publish Thumbnail", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Form", "Comments", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_btn.setText(QtGui.QApplication.translate("Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.publish_btn.setText(QtGui.QApplication.translate("Form", "Publish", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
