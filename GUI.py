# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.UI'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1021, 688)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.mode_string = QtWidgets.QLineEdit(self.centralwidget)
        self.mode_string.setObjectName("mode_string")
        self.gridLayout.addWidget(self.mode_string, 1, 0, 1, 1)
        self.connection_string = QtWidgets.QLineEdit(self.centralwidget)
        self.connection_string.setObjectName("connection_string")
        self.gridLayout.addWidget(self.connection_string, 0, 0, 1, 1)
        self.Cycle_measurement_button = QtWidgets.QPushButton(self.centralwidget)
        self.Cycle_measurement_button.setObjectName("Cycle_measurement_button")
        self.gridLayout.addWidget(self.Cycle_measurement_button, 0, 1, 1, 1)
        self.Connection_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Connection_Button.setMinimumSize(QtCore.QSize(0, 0))
        self.Connection_Button.setBaseSize(QtCore.QSize(0, 0))
        self.Connection_Button.setObjectName("Connection_Button")
        self.gridLayout.addWidget(self.Connection_Button, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1021, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Cycle_measurement_button.setText(_translate("MainWindow", "Запустить измерения"))
        self.Connection_Button.setText(_translate("MainWindow", "Подключить             "))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
