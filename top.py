#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from src.erase.eraseDiskWidget import *
from src.read.readDiskWidget import *
from src.qss.qss import *
from src.wave.waveTop import *
from src.serial.serialTop import *

from src import *


class Top(QMainWindow):
    def __init__(self):
        super(Top, self).__init__()
        self.createToolBar()

        self.initUI()

        self.config = {
            'eraseDisk' : 0,
            'readDisk' : 1,
            'showWave' : 2,
            'serial' : 3
        }

    def initUI(self):
        self.readDiskStack = ReadDiskWidget()
        self.eraseDiskStack = EraseDiskWidget()
        self.waveTopStack = WaveTop()
        self.serialStack = SerialTop()
        self.stack = QStackedWidget()
        self.stack.addWidget(self.eraseDiskStack)
        self.stack.addWidget(self.readDiskStack)
        self.stack.addWidget(self.waveTopStack)
        self.stack.addWidget(self.serialStack)

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
        self.showWaveAction = QAction(QIcon('images/showWave.svg'), "showWave", self, triggered=self.showWidget)
        self.serialAction = QAction(QIcon('images/serialIcon.svg'), "serial", self, triggered=self.showWidget)
        toolBar = QToolBar('Navigation')
        toolBar.addAction(self.eraseDiskAction)
        toolBar.addAction(self.readDiskAction)
        toolBar.addAction(self.showWaveAction)
        # toolBar.addAction(self.serialAction)
        toolBar.setIconSize(QSize(48, 48))
        toolBar.setFixedHeight(48)
        self.addToolBar(toolBar)
        

        # toolbar = self.addToolBar('T')
        # toolbar.addAction(self.eraseDiskAction)
        # toolbar.addAction(self.readDiskAction)
        # toolbar.addAction(self.showWaveAction)


    def showWidget(self):
        sender = self.sender()
        if sender.text() == 'eraseDisk':
            self.stack.setCurrentIndex(self.config['eraseDisk'])
        elif sender.text() == 'readDisk':
            self.stack.setCurrentIndex(self.config['readDisk'])
        elif sender.text() == 'showWave':
            self.stack.setCurrentIndex(self.config['showWave'])
        elif sender.text() == 'serial':
            self.stack.setCurrentIndex(self.config['serial'])
        else:
            pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Top()
    ui.show()

    ui.setStyleSheet(style)
    sys.exit(app.exec_())
