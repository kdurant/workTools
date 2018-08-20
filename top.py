#-*- coding:utf-8 -*-

from src import *



class Top(QMainWindow):
    def __init__(self):
        super(Top, self).__init__()
        self.createToolBar()

        self.initUI()
        self.setWindowTitle('测试工具')
        self.setWindowIcon(QIcon('images/icon.svg'))
        self.resize(QSize(1000, 800))

        self.config = {
            'eraseDisk' : 0,
            'readDisk' : 1,
            'showWave' : 2,
            'serial' : 3,
            'extBoard' : 4,
            'captureBoard' : 5
        }

    def initUI(self):
        self.readDiskStack = ReadDiskWidget()
        self.eraseDiskStack = EraseDiskWidget()
        self.waveTopStack = WaveTop()
        self.serialStack = SerialTop()
        self.extBoardStack = ExtBoard()
        self.captureBoardStack = CaptureBoard()
        self.stack = QStackedWidget()
        self.stack.addWidget(self.eraseDiskStack)
        self.stack.addWidget(self.readDiskStack)
        self.stack.addWidget(self.waveTopStack)
        self.stack.addWidget(self.serialStack)
        self.stack.addWidget(self.extBoardStack)
        self.stack.addWidget(self.captureBoardStack)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.stack)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        pass

    def createToolBar(self):
        self.readDiskAction = QAction(QIcon('images/readDisk.svg'), "readDisk", self, triggered=self.showWidget)
        self.eraseDiskAction = QAction(QIcon('images/eraseDisk.svg'), "eraseDisk", self, triggered=self.showWidget)
        self.showWaveAction = QAction(QIcon('images/showWave.svg'), "showWave", self, triggered=self.showWidget)
        self.serialAction = QAction(QIcon('images/serialIcon.svg'), "serial", self, triggered=self.showWidget)
        self.extBoard = QAction(QIcon('images/extBoard.svg'), "extBoard", self, triggered=self.showWidget)
        self.captureBoard = QAction(QIcon('images/captureBoard.svg'), "captureBoard", self, triggered=self.showWidget)
        toolBar = QToolBar('Navigation')
        toolBar.addAction(self.eraseDiskAction)
        toolBar.addAction(self.readDiskAction)
        toolBar.addAction(self.showWaveAction)
        # toolBar.addAction(self.serialAction)
        toolBar.addAction(self.extBoard)
        toolBar.addAction(self.captureBoard)
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
        elif sender.text() == 'extBoard':
            self.stack.setCurrentIndex(self.config['extBoard'])
        elif sender.text() == 'captureBoard':
            self.stack.setCurrentIndex(self.config['captureBoard'])
        else:
            pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Top()
    ui.show()

    ui.setStyleSheet(style)
    sys.exit(app.exec_())
