# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'watchdog_main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(828, 344)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionimay = QAction(MainWindow)
        self.actionimay.setObjectName(u"actionimay")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_11 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(6, 0, 6, 6)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.MainPage = QWidget()
        self.MainPage.setObjectName(u"MainPage")
        sizePolicy.setHeightForWidth(self.MainPage.sizePolicy().hasHeightForWidth())
        self.MainPage.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.MainPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 3, 6, 6)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.WatchDogList = QTableWidget(self.MainPage)
        if (self.WatchDogList.columnCount() < 7):
            self.WatchDogList.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.WatchDogList.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.WatchDogList.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.WatchDogList.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.WatchDogList.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.WatchDogList.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.WatchDogList.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.WatchDogList.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.WatchDogList.setObjectName(u"WatchDogList")
        self.WatchDogList.horizontalHeader().setCascadingSectionResizes(False)

        self.verticalLayout.addWidget(self.WatchDogList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.CPUusageLabel = QLabel(self.MainPage)
        self.CPUusageLabel.setObjectName(u"CPUusageLabel")

        self.horizontalLayout.addWidget(self.CPUusageLabel)

        self.SystemUsageStateLabel = QLabel(self.MainPage)
        self.SystemUsageStateLabel.setObjectName(u"SystemUsageStateLabel")
        font = QFont()
        font.setItalic(False)
        font.setUnderline(True)
        self.SystemUsageStateLabel.setFont(font)

        self.horizontalLayout.addWidget(self.SystemUsageStateLabel)

        self.MEMusageLabel = QLabel(self.MainPage)
        self.MEMusageLabel.setObjectName(u"MEMusageLabel")

        self.horizontalLayout.addWidget(self.MEMusageLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_10)

        self.UseButton = QPushButton(self.MainPage)
        self.UseButton.setObjectName(u"UseButton")

        self.horizontalLayout.addWidget(self.UseButton)

        self.RemoveButton = QPushButton(self.MainPage)
        self.RemoveButton.setObjectName(u"RemoveButton")

        self.horizontalLayout.addWidget(self.RemoveButton)

        self.ServerUrlButton = QPushButton(self.MainPage)
        self.ServerUrlButton.setObjectName(u"ServerUrlButton")

        self.horizontalLayout.addWidget(self.ServerUrlButton)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_9)

        self.SwitchButton = QPushButton(self.MainPage)
        self.SwitchButton.setObjectName(u"SwitchButton")

        self.horizontalLayout.addWidget(self.SwitchButton)

        self.RestartButton = QPushButton(self.MainPage)
        self.RestartButton.setObjectName(u"RestartButton")

        self.horizontalLayout.addWidget(self.RestartButton)

        self.BrowseButton = QPushButton(self.MainPage)
        self.BrowseButton.setObjectName(u"BrowseButton")

        self.horizontalLayout.addWidget(self.BrowseButton)

        self.ProcessSetupButton = QPushButton(self.MainPage)
        self.ProcessSetupButton.setObjectName(u"ProcessSetupButton")

        self.horizontalLayout.addWidget(self.ProcessSetupButton)

        self.horizontalLayout.setStretch(3, 10)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(9, 1)
        self.horizontalLayout.setStretch(10, 1)
        self.horizontalLayout.setStretch(12, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.stackedWidget.addWidget(self.MainPage)
        self.FullSetupPage = QWidget()
        self.FullSetupPage.setObjectName(u"FullSetupPage")
        sizePolicy.setHeightForWidth(self.FullSetupPage.sizePolicy().hasHeightForWidth())
        self.FullSetupPage.setSizePolicy(sizePolicy)
        self.horizontalLayout_12 = QHBoxLayout(self.FullSetupPage)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.show_version_label = QLabel(self.FullSetupPage)
        self.show_version_label.setObjectName(u"show_version_label")
        font1 = QFont()
        font1.setItalic(True)
        font1.setUnderline(True)
        self.show_version_label.setFont(font1)

        self.horizontalLayout_6.addWidget(self.show_version_label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.horizontalLayout_6.setStretch(0, 5)
        self.horizontalLayout_6.setStretch(1, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.autoStartUpCheckBox = QCheckBox(self.FullSetupPage)
        self.autoStartUpCheckBox.setObjectName(u"autoStartUpCheckBox")

        self.horizontalLayout_7.addWidget(self.autoStartUpCheckBox)

        self.create_start_script_button = QPushButton(self.FullSetupPage)
        self.create_start_script_button.setObjectName(u"create_start_script_button")

        self.horizontalLayout_7.addWidget(self.create_start_script_button)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.FullSetup_HiddenButton = QCheckBox(self.FullSetupPage)
        self.FullSetup_HiddenButton.setObjectName(u"FullSetup_HiddenButton")

        self.horizontalLayout_3.addWidget(self.FullSetup_HiddenButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_5 = QLabel(self.FullSetupPage)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_8.addWidget(self.label_5)

        self.start_way_combobox = QComboBox(self.FullSetupPage)
        self.start_way_combobox.setObjectName(u"start_way_combobox")

        self.horizontalLayout_8.addWidget(self.start_way_combobox)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_12)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 2)
        self.horizontalLayout_8.setStretch(2, 7)

        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.FullSetupPage)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.FullSetupMemComboBox = QComboBox(self.FullSetupPage)
        self.FullSetupMemComboBox.setObjectName(u"FullSetupMemComboBox")

        self.horizontalLayout_2.addWidget(self.FullSetupMemComboBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 4)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.FullSetupPage)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.FullSetupFlushSpin = QDoubleSpinBox(self.FullSetupPage)
        self.FullSetupFlushSpin.setObjectName(u"FullSetupFlushSpin")

        self.horizontalLayout_5.addWidget(self.FullSetupFlushSpin)

        self.label_3 = QLabel(self.FullSetupPage)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 3)
        self.horizontalLayout_5.setStretch(3, 9)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_4 = QLabel(self.FullSetupPage)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_10.addWidget(self.label_4)

        self.FullSetupReopenComboBox = QComboBox(self.FullSetupPage)
        self.FullSetupReopenComboBox.setObjectName(u"FullSetupReopenComboBox")

        self.horizontalLayout_10.addWidget(self.FullSetupReopenComboBox)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_8)

        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 1)
        self.horizontalLayout_10.setStretch(2, 4)

        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_6 = QLabel(self.FullSetupPage)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_9.addWidget(self.label_6)

        self.frpc_path_line_edit = QLineEdit(self.FullSetupPage)
        self.frpc_path_line_edit.setObjectName(u"frpc_path_line_edit")
        self.frpc_path_line_edit.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.frpc_path_line_edit)

        self.frpc_path_button = QPushButton(self.FullSetupPage)
        self.frpc_path_button.setObjectName(u"frpc_path_button")

        self.horizontalLayout_9.addWidget(self.frpc_path_button)

        self.frpc_clear_button = QPushButton(self.FullSetupPage)
        self.frpc_clear_button.setObjectName(u"frpc_clear_button")

        self.horizontalLayout_9.addWidget(self.frpc_clear_button)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_11)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 6)
        self.horizontalLayout_9.setStretch(2, 1)
        self.horizontalLayout_9.setStretch(3, 1)
        self.horizontalLayout_9.setStretch(4, 3)

        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.verticalSpacer = QSpacerItem(17, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.FullSetupBackMainButton = QPushButton(self.FullSetupPage)
        self.FullSetupBackMainButton.setObjectName(u"FullSetupBackMainButton")

        self.horizontalLayout_4.addWidget(self.FullSetupBackMainButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_12.addLayout(self.verticalLayout_3)

        self.stackedWidget.addWidget(self.FullSetupPage)

        self.horizontalLayout_11.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 828, 22))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionimay.setText(QCoreApplication.translate("MainWindow", u"imay ", None))
        ___qtablewidgetitem = self.WatchDogList.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u76d1\u542c", None));
        ___qtablewidgetitem1 = self.WatchDogList.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u8fdb\u7a0b\u540d", None));
        ___qtablewidgetitem2 = self.WatchDogList.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"pid", None));
        ___qtablewidgetitem3 = self.WatchDogList.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u7a0b\u5e8f\u540d", None));
        ___qtablewidgetitem4 = self.WatchDogList.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u5185\u5b58", None));
        ___qtablewidgetitem5 = self.WatchDogList.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u7ebf\u7a0b", None));
        ___qtablewidgetitem6 = self.WatchDogList.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u72b6\u6001", None));
        self.CPUusageLabel.setText(QCoreApplication.translate("MainWindow", u"[CPU]: 00.00%", None))
        self.SystemUsageStateLabel.setText(QCoreApplication.translate("MainWindow", u"|", None))
        self.MEMusageLabel.setText(QCoreApplication.translate("MainWindow", u"[\u5185\u5b58]: 00.00%", None))
        self.UseButton.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528\u770b\u95e8\u72d7", None))
        self.RemoveButton.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u9664", None))
        self.ServerUrlButton.setText(QCoreApplication.translate("MainWindow", u"\u670d\u52a1\u9875\u9762", None))
        self.SwitchButton.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8/\u505c\u6b62", None))
        self.RestartButton.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u542f", None))
        self.BrowseButton.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8", None))
        self.ProcessSetupButton.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.show_version_label.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u7248\u672c: ", None))
        self.autoStartUpCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u673a\u81ea\u52a8\u542f\u52a8(\u8fdb\u5165\u684c\u9762\u751f\u6548)", None))
        self.create_start_script_button.setText(QCoreApplication.translate("MainWindow", u"\u5728\u5f53\u524d\u76ee\u5f55\u751f\u6210\u542f\u52a8\u811a\u672c(\u5230\u8ba1\u5212\u4efb\u52a1\u4e2d\u914d\u7f6e)", None))
        self.FullSetup_HiddenButton.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u540e\u9690\u85cf", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u65b9\u5f0f(\u5b9e\u9a8c\u4e2d)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5168\u5c40\u5185\u5b58\u5355\u4f4d", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0\u65f6\u95f4\u95f4\u9694(\u79d2)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u542f\u540e\u751f\u6548", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u590d\u542f\u52a8\u770b\u95e8\u72d7", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"frpc.toml\u8def\u5f84", None))
        self.frpc_path_button.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8", None))
        self.frpc_clear_button.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
        self.FullSetupBackMainButton.setText(QCoreApplication.translate("MainWindow", u"\u8fd4\u56de\u4e3b\u754c\u9762", None))
    # retranslateUi

