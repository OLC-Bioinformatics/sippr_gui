#!/usr/bin/env python 3
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
import sys
import os
__author__ = 'adamkoziol'

testpath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(testpath, 'demos'))

import popup_error


class PopupError(QDialog, popup_error.Ui_Dialog):

    def add_icon(self):
        self.label.setText('CustomError')
        icon = QtGui.QImage('cowbat.png')
        self.label.setPixmap(QtGui.QPixmap.fromImage(icon))

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.add_icon()
