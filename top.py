#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from src.erase.eraseDiskWidget import *
from src.read.readDiskWidget import *
from src.qss.qss import *

class Top(QMainWindow):
    def __init__(self):
        super(Top, self).__init__()
        self.createToolBar()

        self.initUI()

        self.config = {
            'eraseDisk' : 0,
            'readDisk' : 1
        }

    def initUI(self):
        self.readDiskStack = ReadDiskWidget()
        self.eraseDiskStack = EraseDiskWidget()
        self.stack = QStackedWidget()
        self.stack.addWidget(self.eraseDiskStack)
        self.stack.addWidget(self.readDiskStack)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.stack)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        self.resize(640, 500)
        pass

    def createToolBar(self):
        self.readDiskAction = QAction(QIcon('images/readDisk.svg'), "readDisk", self, triggered=self.showWidget)
        self.eraseDiskAction = QAction(QIcon('images/eraseDisk.svg'), "eraseDisk", self, triggered=self.showWidget)

        toolbar = self.addToolBar('T')
        toolbar.addAction(self.eraseDiskAction)
        toolbar.addAction(self.readDiskAction)


    def showWidget(self):
        sender = self.sender()
        if sender.text() == 'eraseDisk':
            self.stack.setCurrentIndex(self.config['eraseDisk'])
        elif sender.text() == 'readDisk':
            self.stack.setCurrentIndex(self.config['readDisk'])


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Top()
    ui.show()

    ui.setStyleSheet(style)
    sys.exit(app.exec_())
