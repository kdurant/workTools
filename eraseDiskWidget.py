#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class EraseDiskWidget(QWidget):
    def __init__(self):
        super(EraseDiskWidget, self).__init__()

        self.initUI()

    def initUI(self):
        label = QLabel('eraser disk')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(label)

        self.setLayout(mainLayout)
