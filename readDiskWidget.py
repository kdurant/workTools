#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ReadDiskWidget(QWidget):
    def __init__(self):
        super(ReadDiskWidget, self).__init__()

        self.initUI()

    def initUI(self):
        label = QLabel('read disk')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(label)

        self.setLayout(mainLayout)
