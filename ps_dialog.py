# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'process_setup.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(370, 325)
        self.verticalLayout_7 = QVBoxLayout(Dialog)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.OtherNameEdit = QLineEdit(Dialog)
        self.OtherNameEdit.setObjectName(u"OtherNameEdit")

        self.horizontalLayout_3.addWidget(self.OtherNameEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_3.setStretch(0, 8)
        self.horizontalLayout_3.setStretch(1, 2)

        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.exe_label = QLabel(Dialog)
        self.exe_label.setObjectName(u"exe_label")

        self.verticalLayout_2.addWidget(self.exe_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ExePathEdit = QLineEdit(Dialog)
        self.ExePathEdit.setObjectName(u"ExePathEdit")

        self.horizontalLayout.addWidget(self.ExePathEdit)

        self.ExePathButton = QPushButton(Dialog)
        self.ExePathButton.setObjectName(u"ExePathButton")

        self.horizontalLayout.addWidget(self.ExePathButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_5.addWidget(self.label_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.WorkDirEdit = QLineEdit(Dialog)
        self.WorkDirEdit.setObjectName(u"WorkDirEdit")

        self.horizontalLayout_5.addWidget(self.WorkDirEdit)

        self.WorkDirButton = QPushButton(Dialog)
        self.WorkDirButton.setObjectName(u"WorkDirButton")

        self.horizontalLayout_5.addWidget(self.WorkDirButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ArgumentsEdit = QLineEdit(Dialog)
        self.ArgumentsEdit.setObjectName(u"ArgumentsEdit")

        self.horizontalLayout_4.addWidget(self.ArgumentsEdit)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_4.setStretch(0, 8)
        self.horizontalLayout_4.setStretch(1, 2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout_6.addWidget(self.label)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.UrlServiceEdit = QLineEdit(Dialog)
        self.UrlServiceEdit.setObjectName(u"UrlServiceEdit")

        self.horizontalLayout_6.addWidget(self.UrlServiceEdit)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_6.setStretch(0, 8)
        self.horizontalLayout_6.setStretch(1, 2)

        self.verticalLayout_6.addLayout(self.horizontalLayout_6)


        self.verticalLayout_4.addLayout(self.verticalLayout_6)

        self.HiddenCheckBox = QCheckBox(Dialog)
        self.HiddenCheckBox.setObjectName(u"HiddenCheckBox")

        self.verticalLayout_4.addWidget(self.HiddenCheckBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.SaveButton = QPushButton(Dialog)
        self.SaveButton.setObjectName(u"SaveButton")

        self.horizontalLayout_2.addWidget(self.SaveButton)

        self.CancelButton = QPushButton(Dialog)
        self.CancelButton.setObjectName(u"CancelButton")

        self.horizontalLayout_2.addWidget(self.CancelButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.verticalLayout_7.addLayout(self.verticalLayout_4)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u76d1\u542c\u522b\u540d", None))
        self.exe_label.setText(QCoreApplication.translate("Dialog", u"\u53ef\u6267\u884c\u6587\u4ef6\u8def\u5f84", None))
        self.ExePathButton.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u5de5\u4f5c\u76ee\u5f55", None))
        self.WorkDirButton.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u542f\u52a8\u53c2\u6570", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u670d\u52a1\u5730\u5740(\u9009\u586b)", None))
        self.HiddenCheckBox.setText(QCoreApplication.translate("Dialog", u"\u9690\u85cf\u7a97\u53e3(\u4ec5\u5bf9\u63a7\u5236\u53f0\u7a0b\u5e8f\u6709\u6548)", None))
        self.SaveButton.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58", None))
        self.CancelButton.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

