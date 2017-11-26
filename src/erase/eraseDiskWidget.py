#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

FILE_UNIT = 0x5000

class EraseDiskWidget(QWidget):
    def __init__(self):
        super(EraseDiskWidget, self).__init__()

        self.initUI()

        self.eraseBtn.clicked.connect(self.eraseFileNameRegion)

    def initUI(self):
        self.diskSelectComb = QComboBox()
        self.diskSelectComb.addItems(self.diskInfo())
        self.eraseBtn = QPushButton('擦除文件名区域')

        self.label = QLabel('擦除进度：')
        self.progress = QProgressBar()
        self.progress.setMaximum(FILE_UNIT-1)
        self.progress.setMinimum(0)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.diskSelectComb)
        mainLayout.addWidget(self.eraseBtn)
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.progress)

        self.setLayout(mainLayout)

    def eraseFileNameRegion(self):
        reply = QMessageBox.critical(self, 'Critical', '擦除文件名区域', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.eraseSector()
        else:
            pass

    @staticmethod
    def diskInfo():
        info = []
        try:
            disk = open('\\\\.\\PHYSICALDRIVE0', 'rb')
        except PermissionError:
            info.append('\\\\.\\PHYSICALDRIVE0')
        try:
            disk = open('\\\\.\\PHYSICALDRIVE1', 'rb')
        except PermissionError:
            info.append('\\\\.\\PHYSICALDRIVE1')

        return info

    def eraseSector(self):
        import time
        for i in range(0, FILE_UNIT):
            time.sleep(0.001)
            print(i)
            self.progress.setValue(i)
        pass
