# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'genesippr.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GeneSippr(object):
    def setupUi(self, GeneSippr):
        GeneSippr.setObjectName("GeneSippr")
        GeneSippr.resize(820, 549)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GeneSippr.sizePolicy().hasHeightForWidth())
        GeneSippr.setSizePolicy(sizePolicy)
        GeneSippr.setMaximumSize(QtCore.QSize(1920, 1080))
        self.centralwidget = QtWidgets.QWidget(GeneSippr)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.forwardreads = QtWidgets.QLabel(self.centralwidget)
        self.forwardreads.setObjectName("forwardreads")
        self.gridLayout.addWidget(self.forwardreads, 2, 0, 1, 1)
        self.output = QtWidgets.QTextBrowser(self.centralwidget)
        self.output.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.output.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.output.setObjectName("output")
        self.gridLayout.addWidget(self.output, 5, 0, 1, 1)
        self.reversereads = QtWidgets.QLabel(self.centralwidget)
        self.reversereads.setObjectName("reversereads")
        self.gridLayout.addWidget(self.reversereads, 3, 0, 1, 1)
        self.analysis_btn = QtWidgets.QPushButton(self.centralwidget)
        self.analysis_btn.setEnabled(False)
        self.analysis_btn.setObjectName("analysis_btn")
        self.gridLayout.addWidget(self.analysis_btn, 4, 0, 1, 1)
        self.miseq_folder_btn = QtWidgets.QPushButton(self.centralwidget)
        self.miseq_folder_btn.setEnabled(True)
        self.miseq_folder_btn.setObjectName("miseq_folder_btn")
        self.gridLayout.addWidget(self.miseq_folder_btn, 0, 0, 1, 1)
        self.reports = QtWidgets.QPushButton(self.centralwidget)
        self.reports.setEnabled(False)
        self.reports.setObjectName("reports")
        self.gridLayout.addWidget(self.reports, 6, 0, 1, 1)
        self.run_name = QtWidgets.QLabel(self.centralwidget)
        self.run_name.setObjectName("run_name")
        self.gridLayout.addWidget(self.run_name, 1, 0, 1, 1)
        GeneSippr.setCentralWidget(self.centralwidget)

        self.retranslateUi(GeneSippr)
        QtCore.QMetaObject.connectSlotsByName(GeneSippr)

    def retranslateUi(self, GeneSippr):
        _translate = QtCore.QCoreApplication.translate
        GeneSippr.setWindowTitle(_translate("GeneSippr", "GeneSippr"))
        self.forwardreads.setText(_translate("GeneSippr", "Forward Read Length: "))
        self.reversereads.setText(_translate("GeneSippr", "Reverse Read Length: "))
        self.analysis_btn.setText(_translate("GeneSippr", "Run"))
        self.miseq_folder_btn.setText(_translate("GeneSippr", "MiSeqFolder"))
        self.reports.setText(_translate("GeneSippr", "Reports"))
        self.run_name.setText(_translate("GeneSippr", "MiSeq Run Name:"))

