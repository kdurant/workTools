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
        self.udpConfig()
        self.signalSlot()

    def udpConfig(self):
        self.udpSocket = QUdpSocket(self)
        status = self.udpSocket.bind(int(self.masterPort.text()))
        if status:
            self.udpSocket.readyRead.connect(self.processPendingDatagrams)
        else:
            QMessageBox.warning(self, "警告", 'UDP端口被占用')

    def initUI(self):
        self.sendCommand = CommandTest()
        self.info = self.sysParameterUI()
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
        leftLayout.addWidget(self.info)
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

    def sysParameterUI(self):
        groupBox = QGroupBox('参数设置')
        self.masterIP = QLineEdit('192.168.1.166')
        self.masterIP.setReadOnly(True)
        self.masterPort = QLineEdit('6666')
        self.masterPort.setReadOnly(True)

        self.targetIP = QLineEdit('192.168.1.102')
        self.targetPort = QLineEdit('4444')

        self.bindLabel = QLabel()
        self.bindLabel.setPixmap(QPixmap('images/inactive.svg').scaled(QSize(24, 24)))
        self.bindBtn = QPushButton('已经断开')
        #
        # label = QLabel()
        # label.setPixmap(QPixmap('images/debug.svg').scaled(QSize(150, 150)))

        form = QFormLayout()
        form.addRow('本机IP地址：', self.masterIP)
        form.addRow('本机端口号：', self.masterPort)
        form.addRow('设备IP地址：', self.targetIP)
        form.addRow('UDP端口号：', self.targetPort)
        form.addRow(self.bindBtn, self.bindLabel)

        hbox = QHBoxLayout()
        hbox.addLayout(form)
        hbox.addStretch(1)
        # hbox.addWidget(label)
        # hbox.addStretch(1)

        groupBox.setLayout(hbox)
        return groupBox

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

        self.bindBtn.clicked.connect(self.udpLinkStatus)
        # self.send_btn.clicked.connect(self.configUdpFrame)
        self.clearBtn.clicked.connect(self.recDataEdit.clear)

        self.sendCommand.packetFrameDone[str].connect(self.sendUdpFrame)
        self.dacTest.packetFrameDone[str].connect(self.sendUdpFrame)
        self.adcTest.packetFrameDone[str].connect(self.sendUdpFrame)
        self.motorTest.packetFrameDone[str].connect(self.sendUdpFrame)
        self.laserTest.packetFrameDone[str].connect(self.sendUdpFrame)


        self.dataToADC[str].connect(self.adcTest.processFrame)
        self.dataToMotor[str].connect(self.motorTest.processFrame)
        self.dataToLaser[str].connect(self.laserTest.processFrame)
        self.dataToGPS[str].connect(self.gpsTest.processFrame)

    @pyqtSlot(str)
    def sendUdpFrame(self, frame):
        self.udpSocket.writeDatagram(QByteArray(a2b_hex(frame)), QHostAddress(self.targetIP.text()),
                                     int(self.targetPort.text()))

    @pyqtSlot()
    def processPendingDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            datagram = b2a_hex(datagram)
            datagram = datagram.decode(encoding = 'utf-8')
            # print(datagram)
            if self.bindBtn.text() == '已经连接':
                if datagram[24:32] != '80000001':
                    self.recDataEdit.append(datagram)

                if datagram[24:32] == '80000016':
                    self.dataToADC.emit(datagram)
                elif datagram[24:32] == '8000000c':
                    self.dataToMotor.emit(datagram)
                elif datagram[24:32] == '80000003':
                    self.dataToLaser.emit(datagram)
                elif datagram[24:32] == '80000002':
                    self.dataToGPS.emit(datagram)
                    print(datagram)

    @pyqtSlot()
    def udpLinkStatus(self):
        if self.bindBtn.text() == '已经断开':
            self.bindBtn.setText('已经连接')
            self.bindLabel.setPixmap(QPixmap('images/active.svg').scaled(QSize(24, 24)))
        else:
            self.bindBtn.setText('已经断开')
            self.bindLabel.setPixmap(QPixmap('images/inactive.svg').scaled(QSize(24, 24)))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ExtBoard()
    ui.show()
    sys.exit(app.exec_())
