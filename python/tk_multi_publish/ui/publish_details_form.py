# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'publish_details_form.ui'
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


from ..publish_details_form import ThumbnailWidget

from  . import resources_rc

class Ui_PublishDetailsForm(object):
    def setupUi(self, PublishDetailsForm):
        if not PublishDetailsForm.objectName():
            PublishDetailsForm.setObjectName(u"PublishDetailsForm")
        PublishDetailsForm.resize(771, 540)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PublishDetailsForm.sizePolicy().hasHeightForWidth())
        PublishDetailsForm.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(PublishDetailsForm)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.items_title_label = QLabel(PublishDetailsForm)
        self.items_title_label.setObjectName(u"items_title_label")
        self.items_title_label.setStyleSheet(u"#items_title_label {\n"
"font-size: 14px\n"
"}")
        self.items_title_label.setIndent(4)

        self.verticalLayout_7.addWidget(self.items_title_label)

        self.publishes_stacked_widget = QStackedWidget(PublishDetailsForm)
        self.publishes_stacked_widget.setObjectName(u"publishes_stacked_widget")
        self.publishes_stacked_widget.setStyleSheet(u"")
        self.publishes_page = QWidget()
        self.publishes_page.setObjectName(u"publishes_page")
        self.horizontalLayout_7 = QHBoxLayout(self.publishes_page)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.task_scroll = QScrollArea(self.publishes_page)
        self.task_scroll.setObjectName(u"task_scroll")
        self.task_scroll.setStyleSheet(u"#task_scroll {\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2px;\n"
"border-color: rgb(32,32,32);\n"
"}")
        self.task_scroll.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 98, 28))
        self.task_scroll.setWidget(self.contents)

        self.horizontalLayout_7.addWidget(self.task_scroll)

        self.publishes_stacked_widget.addWidget(self.publishes_page)
        self.no_publishes_page = QWidget()
        self.no_publishes_page.setObjectName(u"no_publishes_page")
        self.no_publishes_page.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.no_publishes_page)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.no_publishes_frame = QFrame(self.no_publishes_page)
        self.no_publishes_frame.setObjectName(u"no_publishes_frame")
        self.no_publishes_frame.setStyleSheet(u"#no_publishes_frame {\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2px;\n"
"border-color: rgb(32,32,32);\n"
"}")
        self.no_publishes_frame.setFrameShape(QFrame.StyledPanel)
        self.no_publishes_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.no_publishes_frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(0, 88, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_6 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)

        self.label_3 = QLabel(self.no_publishes_frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setWordWrap(True)

        self.horizontalLayout_9.addWidget(self.label_3)

        self.horizontalSpacer_7 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)

        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.verticalSpacer_2 = QSpacerItem(0, 88, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.verticalLayout_2.addWidget(self.no_publishes_frame)

        self.publishes_stacked_widget.addWidget(self.no_publishes_page)

        self.verticalLayout_7.addWidget(self.publishes_stacked_widget)

        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.info_title_label = QLabel(PublishDetailsForm)
        self.info_title_label.setObjectName(u"info_title_label")
        self.info_title_label.setStyleSheet(u"#info_title_label {\n"
"font-size: 14px\n"
"}")
        self.info_title_label.setIndent(4)

        self.verticalLayout_5.addWidget(self.info_title_label)

        self.info_frame = QFrame(PublishDetailsForm)
        self.info_frame.setObjectName(u"info_frame")
        self.info_frame.setStyleSheet(u"#info_frame {\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2px;\n"
"border-color: rgb(32,32,32);\n"
"}")
        self.info_frame.setFrameShape(QFrame.StyledPanel)
        self.info_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.info_frame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.task_header_label = QLabel(self.info_frame)
        self.task_header_label.setObjectName(u"task_header_label")
        self.task_header_label.setStyleSheet(u"QLabel {\n"
"font-size: 12px;\n"
"}")

        self.verticalLayout_6.addWidget(self.task_header_label)

        self.sg_task_stacked_widget = QStackedWidget(self.info_frame)
        self.sg_task_stacked_widget.setObjectName(u"sg_task_stacked_widget")
        self.sg_task_menu_page = QWidget()
        self.sg_task_menu_page.setObjectName(u"sg_task_menu_page")
        self.horizontalLayout_4 = QHBoxLayout(self.sg_task_menu_page)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.sg_task_combo = QComboBox(self.sg_task_menu_page)
        self.sg_task_combo.setObjectName(u"sg_task_combo")

        self.horizontalLayout_4.addWidget(self.sg_task_combo)

        self.sg_task_stacked_widget.addWidget(self.sg_task_menu_page)
        self.sg_task_label_page = QWidget()
        self.sg_task_label_page.setObjectName(u"sg_task_label_page")
        self.horizontalLayout_5 = QHBoxLayout(self.sg_task_label_page)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.sg_task_label = QLabel(self.sg_task_label_page)
        self.sg_task_label.setObjectName(u"sg_task_label")
        self.sg_task_label.setIndent(12)

        self.horizontalLayout_5.addWidget(self.sg_task_label)

        self.sg_task_stacked_widget.addWidget(self.sg_task_label_page)

        self.verticalLayout_6.addWidget(self.sg_task_stacked_widget)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.label_7 = QLabel(self.info_frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"QLabel {\n"
"font-size: 12px;\n"
"}")

        self.verticalLayout_6.addWidget(self.label_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.thumbnail_frame = QFrame(self.info_frame)
        self.thumbnail_frame.setObjectName(u"thumbnail_frame")
        self.thumbnail_frame.setStyleSheet(u"#thumbnail_frame {\n"
"border-style: solid;\n"
"border-color: rgb(32,32,32);\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"background: rgb(117,117,117);\n"
"}")
        self.thumbnail_frame.setFrameShape(QFrame.StyledPanel)
        self.thumbnail_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.thumbnail_frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.thumbnail_widget = ThumbnailWidget(self.thumbnail_frame)
        self.thumbnail_widget.setObjectName(u"thumbnail_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.thumbnail_widget.sizePolicy().hasHeightForWidth())
        self.thumbnail_widget.setSizePolicy(sizePolicy1)
        self.thumbnail_widget.setMinimumSize(QSize(200, 150))
        self.thumbnail_widget.setMaximumSize(QSize(200, 150))
        self.thumbnail_widget.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.thumbnail_widget)

        self.horizontalLayout_6.addWidget(self.thumbnail_frame)

        self.horizontalSpacer_4 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.label_8 = QLabel(self.info_frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"QLabel {\n"
"font-size: 12px;\n"
"}")

        self.verticalLayout_6.addWidget(self.label_8)

        self.comments_edit = QTextEdit(self.info_frame)
        self.comments_edit.setObjectName(u"comments_edit")
        self.comments_edit.setMinimumSize(QSize(300, 0))

        self.verticalLayout_6.addWidget(self.comments_edit)

        self.verticalLayout_6.setStretch(6, 1)

        self.verticalLayout_5.addWidget(self.info_frame)

        self.verticalLayout_5.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.cancel_btn = QPushButton(PublishDetailsForm)
        self.cancel_btn.setObjectName(u"cancel_btn")
        self.cancel_btn.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_2.addWidget(self.cancel_btn)

        self.publish_btn = QPushButton(PublishDetailsForm)
        self.publish_btn.setObjectName(u"publish_btn")
        self.publish_btn.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_2.addWidget(self.publish_btn)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(PublishDetailsForm)

        self.publishes_stacked_widget.setCurrentIndex(1)
        self.sg_task_stacked_widget.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(PublishDetailsForm)
    # setupUi

    def retranslateUi(self, PublishDetailsForm):
        PublishDetailsForm.setWindowTitle(QCoreApplication.translate("PublishDetailsForm", u"Form", None))
        self.items_title_label.setText(QCoreApplication.translate("PublishDetailsForm", u"Choose Additional Items to Publish:", None))
        self.label_3.setText(QCoreApplication.translate("PublishDetailsForm", u"<i>This publisher does not have any optional items to choose from.<br><br>Only your current work file will be published.</i>", None))
        self.info_title_label.setText(QCoreApplication.translate("PublishDetailsForm", u"Add Information about your Publish:", None))
        self.task_header_label.setText(QCoreApplication.translate("PublishDetailsForm", u"What Shotgun Task are you working on?", None))
        self.sg_task_label.setText(QCoreApplication.translate("PublishDetailsForm", u"Anm, Animation", None))
        self.label_7.setText(QCoreApplication.translate("PublishDetailsForm", u"Add a Thumbnail?", None))
        self.label_8.setText(QCoreApplication.translate("PublishDetailsForm", u"Any Comments?", None))
        self.cancel_btn.setText(QCoreApplication.translate("PublishDetailsForm", u"Cancel", None))
        self.publish_btn.setText(QCoreApplication.translate("PublishDetailsForm", u"Publish", None))
    # retranslateUi
