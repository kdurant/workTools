#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from binascii import a2b_hex, b2a_hex

class NetConfigWidget(QWidget):
    udpRecvDataReady = pyqtSignal(str)
    tcpRecvDataReady = pyqtSignal(str)
    def __init__(self):
        super(NetConfigWidget, self).__init__()
        self.initUI()
        self.signalSlot()

    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.paraUI())
        self.setLayout(mainLayout)

    def paraUI(self):
        groupBox = QGroupBox('参数设置')
        self.netSelectComb = QComboBox()
        self.netSelectComb.addItems(['UDP', 'TCP Client', 'TCP Server'])
        self.masterIP = QLineEdit('192.168.1.166')
        # self.masterIP = QLineEdit()
        self.masterIP.setInputMask('000.000.000.000')
        # self.masterIP.setValidator(QRegExpValidator(QRegExp("^((2[0-4]\\d|25[0-5]|[01]?\\d\\d?)\\.){3}(2[0-4]\\d|25[0-5]|[01]?\\d\\d?)$")))
        # self.masterIP.setReadOnly(True)
        self.masterPort = QLineEdit('6666')

        self.targetIP = QLineEdit('192.168.1.102')
        self.targetIP.setInputMask('000.000.000.000')
        self.targetPort = QLineEdit('4444')

        self.bindLabel = QLabel()
        self.bindLabel.setPixmap(QPixmap('images/inactive.svg').scaled(QSize(24, 24)))
        self.bindBtn = QPushButton('已经断开')
        #
        # label = QLabel()
        # label.setPixmap(QPixmap('images/debug.svg').scaled(QSize(150, 150)))

        form = QFormLayout()
        form.addRow('网络类型：', self.netSelectComb)
        form.addRow('本机IP地址：', self.masterIP)
        form.addRow('本机端口号：', self.masterPort)
        form.addRow('设备IP地址：', self.targetIP)
        form.addRow('UDP端口号：', self.targetPort)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.bindBtn)
        hbox.addWidget(self.bindLabel)
        hbox.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(form)
        mainLayout.addLayout(hbox)

        groupBox.setLayout(mainLayout)
        return groupBox

    def signalSlot(self):
        self.bindBtn.clicked.connect(self.udpLinkStatus)

    def udpConfig(self):
        self.udpSocket = QUdpSocket(self)
        status = self.udpSocket.bind(int(self.masterPort.text()))
        if status:
            self.udpSocket.readyRead.connect(self.processUDPDatagrams)
        else:
            QMessageBox.warning(self, "警告", 'UDP端口被占用')

    @pyqtSlot(str)
    def sendUdpFrame(self, frame):
        self.udpSocket.writeDatagram(QByteArray(a2b_hex(frame)), QHostAddress(self.targetIP.text()),
                                     int(self.targetPort.text()))

    @pyqtSlot()
    def processUDPDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            datagram = b2a_hex(datagram)
            datagram = datagram.decode(encoding = 'utf-8')
            # print(datagram)
            self.udpRecvDataReady.emit(datagram)

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
    ui = NetConfigWidget()
    ui.show()
    sys.exit(app.exec_())