# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'publish_result_form.ui'
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

class Ui_PublishResultForm(object):
    def setupUi(self, PublishResultForm):
        if not PublishResultForm.objectName():
            PublishResultForm.setObjectName(u"PublishResultForm")
        PublishResultForm.resize(548, 384)
        self.verticalLayout_4 = QVBoxLayout(PublishResultForm)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_2 = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.status_icon = QLabel(PublishResultForm)
        self.status_icon.setObjectName(u"status_icon")
        self.status_icon.setMinimumSize(QSize(80, 80))
        self.status_icon.setMaximumSize(QSize(80, 80))
        self.status_icon.setBaseSize(QSize(32, 32))
        self.status_icon.setPixmap(QPixmap(u":/res/success.png"))
        self.status_icon.setScaledContents(False)
        self.status_icon.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.status_icon)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.status_title = QLabel(PublishResultForm)
        self.status_title.setObjectName(u"status_title")
        self.status_title.setStyleSheet(u"#status_title {\n"
"font-size: 24px;\n"
"}")

        self.verticalLayout_3.addWidget(self.status_title)

        self.status_details = QLabel(PublishResultForm)
        self.status_details.setObjectName(u"status_details")
        self.status_details.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.status_details.setWordWrap(True)
        self.status_details.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.status_details)

        self.verticalLayout_3.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(2, 3)
        self.horizontalLayout.setStretch(3, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 97, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.close_btn = QPushButton(PublishResultForm)
        self.close_btn.setObjectName(u"close_btn")

        self.horizontalLayout_2.addWidget(self.close_btn)

        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalLayout_4.setStretch(2, 1)

        self.retranslateUi(PublishResultForm)

        QMetaObject.connectSlotsByName(PublishResultForm)
    # setupUi

    def retranslateUi(self, PublishResultForm):
        PublishResultForm.setWindowTitle(QCoreApplication.translate("PublishResultForm", u"Form", None))
        self.status_icon.setText("")
        self.status_title.setText(QCoreApplication.translate("PublishResultForm", u"Success!", None))
        self.status_details.setText(QCoreApplication.translate("PublishResultForm", u"Details...", None))
        self.close_btn.setText(QCoreApplication.translate("PublishResultForm", u"Close", None))
    # retranslateUi
