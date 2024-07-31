# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'publish_form.ui'
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


from ..publish_details_form import PublishDetailsForm
from ..publish_result_form import PublishResultForm
from ..publish_progress_form import PublishProgressForm

from  . import resources_rc

class Ui_PublishForm(object):
    def setupUi(self, PublishForm):
        if not PublishForm.objectName():
            PublishForm.setObjectName(u"PublishForm")
        PublishForm.resize(794, 549)
        PublishForm.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(PublishForm)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.primary_icon_label = QLabel(PublishForm)
        self.primary_icon_label.setObjectName(u"primary_icon_label")
        self.primary_icon_label.setMinimumSize(QSize(80, 80))
        self.primary_icon_label.setMaximumSize(QSize(80, 80))
        self.primary_icon_label.setBaseSize(QSize(32, 32))
        self.primary_icon_label.setPixmap(QPixmap(u":/res/default_header.png"))
        self.primary_icon_label.setScaledContents(False)
        self.primary_icon_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.primary_icon_label)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.verticalLayout_3.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
#ifndef Q_OS_MAC
        self.verticalLayout_2.setSpacing(6)
#endif
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.primary_details_label = QLabel(PublishForm)
        self.primary_details_label.setObjectName(u"primary_details_label")
        self.primary_details_label.setStyleSheet(u"#primary_details_label {\n"
"}")
        self.primary_details_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.primary_details_label.setMargin(0)

        self.verticalLayout_2.addWidget(self.primary_details_label)

        self.primary_error_label = QLabel(PublishForm)
        self.primary_error_label.setObjectName(u"primary_error_label")
        self.primary_error_label.setMinimumSize(QSize(0, 0))
        self.primary_error_label.setStyleSheet(u"")
        self.primary_error_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.primary_error_label.setWordWrap(True)
        self.primary_error_label.setMargin(0)

        self.verticalLayout_2.addWidget(self.primary_error_label)

        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pages = QStackedWidget(PublishForm)
        self.pages.setObjectName(u"pages")
        self.publish_details = PublishDetailsForm()
        self.publish_details.setObjectName(u"publish_details")
        self.pages.addWidget(self.publish_details)
        self.publish_progress = PublishProgressForm()
        self.publish_progress.setObjectName(u"publish_progress")
        self.pages.addWidget(self.publish_progress)
        self.publish_result = PublishResultForm()
        self.publish_result.setObjectName(u"publish_result")
        self.pages.addWidget(self.publish_result)

        self.verticalLayout.addWidget(self.pages)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(PublishForm)

        self.pages.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(PublishForm)
    # setupUi

    def retranslateUi(self, PublishForm):
        PublishForm.setWindowTitle(QCoreApplication.translate("PublishForm", u"Form", None))
        self.primary_icon_label.setText("")
        self.primary_details_label.setText(QCoreApplication.translate("PublishForm", u"<span style='font-size: 16px'}><b>Output Name</b></span><span style='font-size: 12px'}><br>Description...<br>the third line...</span>", None))
        self.primary_error_label.setText(QCoreApplication.translate("PublishForm", u"<html><head/><body><p><span style=\" color:#ffa500;\">Validation Name</span><br/>Details on how to fix etc.</p></body></html>", None))
    # retranslateUi
