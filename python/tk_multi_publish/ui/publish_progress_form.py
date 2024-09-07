# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'publish_progress_form.ui'
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

class Ui_PublishProgressForm(object):
    def setupUi(self, PublishProgressForm):
        if not PublishProgressForm.objectName():
            PublishProgressForm.setObjectName(u"PublishProgressForm")
        PublishProgressForm.resize(651, 384)
        self.verticalLayout_4 = QVBoxLayout(PublishProgressForm)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout_3 = QVBoxLayout()
#ifndef Q_OS_MAC
        self.verticalLayout_3.setSpacing(-1)
#endif
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_2 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.title = QLabel(PublishProgressForm)
        self.title.setObjectName(u"title")
        self.title.setStyleSheet(u"#title {\n"
"font-size: 24px;\n"
"}")

        self.verticalLayout_3.addWidget(self.title)

        self.progress_bar = QProgressBar(PublishProgressForm)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(24)

        self.verticalLayout_3.addWidget(self.progress_bar)

        self.details = QLabel(PublishProgressForm)
        self.details.setObjectName(u"details")
        self.details.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.details.setWordWrap(False)

        self.verticalLayout_3.addWidget(self.details)

        self.stage_progress_bar = QProgressBar(PublishProgressForm)
        self.stage_progress_bar.setObjectName(u"stage_progress_bar")
        self.stage_progress_bar.setValue(24)

        self.verticalLayout_3.addWidget(self.stage_progress_bar)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.verticalLayout_3.setStretch(5, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalLayout_4.setStretch(0, 1)

        self.retranslateUi(PublishProgressForm)

        QMetaObject.connectSlotsByName(PublishProgressForm)
    # setupUi

    def retranslateUi(self, PublishProgressForm):
        PublishProgressForm.setWindowTitle(QCoreApplication.translate("PublishProgressForm", u"Form", None))
        self.title.setText(QCoreApplication.translate("PublishProgressForm", u"Publishing...", None))
        self.details.setText(QCoreApplication.translate("PublishProgressForm", u"(Details)", None))
    # retranslateUi
