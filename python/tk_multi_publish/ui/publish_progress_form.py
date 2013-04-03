# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_progress_form.ui'
#
# Created: Wed Apr  3 16:46:44 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PublishProgressForm(object):
    def setupUi(self, PublishProgressForm):
        PublishProgressForm.setObjectName("PublishProgressForm")
        PublishProgressForm.resize(494, 386)
        self.verticalLayout_4 = QtGui.QVBoxLayout(PublishProgressForm)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QtGui.QSpacerItem(20, 97, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.status_title = QtGui.QLabel(PublishProgressForm)
        self.status_title.setStyleSheet("#status_title {\n"
"font-size: 24px;\n"
"}")
        self.status_title.setObjectName("status_title")
        self.verticalLayout_3.addWidget(self.status_title)
        self.status_details = QtGui.QLabel(PublishProgressForm)
        self.status_details.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.status_details.setWordWrap(False)
        self.status_details.setObjectName("status_details")
        self.verticalLayout_3.addWidget(self.status_details)
        self.progressBar = QtGui.QProgressBar(PublishProgressForm)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.verticalLayout_3.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        spacerItem3 = QtGui.QSpacerItem(20, 97, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)

        self.retranslateUi(PublishProgressForm)
        QtCore.QMetaObject.connectSlotsByName(PublishProgressForm)

    def retranslateUi(self, PublishProgressForm):
        PublishProgressForm.setWindowTitle(QtGui.QApplication.translate("PublishProgressForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.status_title.setText(QtGui.QApplication.translate("PublishProgressForm", "Publishing...", None, QtGui.QApplication.UnicodeUTF8))
        self.status_details.setText(QtGui.QApplication.translate("PublishProgressForm", "(Details)", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
from . import resources_rc
