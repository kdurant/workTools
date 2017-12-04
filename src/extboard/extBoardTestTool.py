from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis
from binascii import a2b_hex, b2a_hex

from .dacWidget import *
from .adcWidget import *
from .motorTest import *
from .laserTest import *
from .gpsTest import *
from .commandTest import *
from .udpCore import UdpCore

class ExtBoard(QMainWindow):
    dataToDAC = pyqtSignal(str)
    dataToADC = pyqtSignal(str)
    dataToMotor = pyqtSignal(str)
    dataToGPS = pyqtSignal(str)
    dataToLaser = pyqtSignal(str)
    def __init__(self):
        super(ExtBoard, self).__init__()
        self.setWindowTitle('扩展板测试工具')
        self.setWindowIcon(QIcon('images/network.svg'))
        self.resize(QSize(800, 700))

        self.cmdCnt = 0
        self.frame = ''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

        # pe = QPalette()
        # self.setAutoFillBackground(True)
        # pe.setColor(QPalette.Window, QColor(185, 185, 185))
        # self.setPalette(pe)

        self.adSampleLen = '160'

        self.initUI()
        self.signalSlot()

    def initUI(self):
        self.sendCommand = CommandTest()
        self.udpCore = UdpCore()
        self.rec_data = self.receiveDataUI()
        self.dacTest = dacWidget()
        self.adcTest = adcWidget()
        self.motorTest = MotorTest()
        self.laserTest = LaserTest()
        self.gpsTest = GpsTest()
        self.tab = QTabWidget()
        self.tab.addTab(self.dacTest, 'DAC测试')
        self.tab.addTab(self.adcTest, 'ADC测试')
        self.tab.addTab(self.motorTest, '电机测试')
        self.tab.addTab(self.laserTest, '激光器测试')
        self.tab.addTab(self.gpsTest, 'GPS测试')

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.udpCore)
        leftLayout.addWidget(self.sendCommand)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.tab)
        rightLayout.addStretch()

        upLayout = QHBoxLayout()
        upLayout.addLayout(leftLayout)
        upLayout.addLayout(rightLayout)
        upLayout.setStretchFactor(leftLayout, 1)
        upLayout.setStretchFactor(rightLayout, 3)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(upLayout)

        mainLayout.addWidget(self.rec_data)
        mainLayout.setStretchFactor(leftLayout, 1)
        # mainLayout.setStretchFactor(right_hbox, 2)

        self.mainFrame = QWidget(self)
        self.mainFrame.setLayout(mainLayout)
        self.setCentralWidget(self.mainFrame)

    def receiveDataUI(self):
        group = QGroupBox('接受数据')
        self.recDataEdit = QTextEdit()
        self.recDataEdit.setReadOnly(True)
        self.clearBtn = QPushButton()
        self.clearBtn.setIcon(QIcon('images/clear.svg'))

        layout = QVBoxLayout()
        layout.addWidget(self.recDataEdit)
        layout.addWidget(self.clearBtn)
        group.setLayout(layout)
        return group
    def signalSlot(self):

        self.clearBtn.clicked.connect(self.recDataEdit.clear)

        self.sendCommand.packetFrameDone[str].connect(self.udpCore.sendFrame)
        self.dacTest.packetFrameDone[str].connect(self.udpCore.sendFrame)
        self.adcTest.packetFrameDone[str].connect(self.udpCore.sendFrame)
        self.motorTest.packetFrameDone[str].connect(self.udpCore.sendFrame)
        self.laserTest.packetFrameDone[str].connect(self.udpCore.sendFrame)

        self.udpCore.recvDataReady[bytes, str, int].connect(self.processPendingDatagrams)
        self.dataToADC[str].connect(self.adcTest.processFrame)
        self.dataToMotor[str].connect(self.motorTest.processFrame)
        self.dataToLaser[str].connect(self.laserTest.processFrame)
        self.dataToGPS[str].connect(self.gpsTest.processFrame)

    @pyqtSlot(bytes, str, int)
    def processPendingDatagrams(self, datagram, host, port):
            data = b2a_hex(datagram)
            data = data.decode(encoding = 'utf-8')
            if self.bindBtn.text() == '已经连接':
                if data[24:32] != '80000001':
                    self.recDataEdit.append(data)

                if data[24:32] == '80000016':
                    self.dataToADC.emit(data)
                elif data[24:32] == '8000000c':
                    self.dataToMotor.emit(data)
                elif data[24:32] == '80000003':
                    self.dataToLaser.emit(data)
                elif data[24:32] == '80000002':
                    self.dataToGPS.emit(data)
                    print(data)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ExtBoard()
    ui.show()
    sys.exit(app.exec_())
