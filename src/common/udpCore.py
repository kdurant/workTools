#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QAbstractSocket, QHostAddress
from binascii import a2b_hex, b2a_hex


class UdpCore(QWidget):
    '''
    UDP作为Server，只需要绑定本机IP地址和端口号，Client发送数据时，指定正确的地址和端口号即可
    '''
    recvDataReady = pyqtSignal(bytes, str, int)
    def __init__(self):
        super(UdpCore, self).__init__()
        self.initUI()

        '''
        disconnectFromHost, close, abort好像都可以中断udp bind状态
        '''
        self.udpSocket = QUdpSocket(self)
        self.signalSlot()

    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.paraUI())
        self.setLayout(mainLayout)

    def paraUI(self):
        groupBox = QGroupBox('参数设置')
        self.masterIP = QLineEdit('192.168.1.166')
        # self.masterIP = QLineEdit('127.0.0.1')
        self.masterIP.setInputMask('000.000.000.000')
        self.masterIP.setToolTip('接收数据时，其他设备需要匹配本机IP地址和端口号')
        self.masterPort = QLineEdit('6666')

        self.targetIP = QLineEdit('192.168.1.102')
        # self.targetIP = QLineEdit('127.0.0.1')
        self.targetIP.setInputMask('000.000.000.000')
        self.targetIP.setToolTip('发送数据时，本机需要匹配其他设备IP地址和端口号')
        self.targetPort = QLineEdit('4444')

        self.bindRbtn = QRadioButton()
        self.bindRbtn.setObjectName('singleRadioBtn')

        form = QFormLayout()
        form.addRow('本机IP地址：', self.masterIP)
        form.addRow('本机端口号：', self.masterPort)
        form.addRow('设备IP地址：', self.targetIP)
        form.addRow('UDP端口号：', self.targetPort)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.bindRbtn)
        hbox.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(form)
        mainLayout.addLayout(hbox)

        groupBox.setLayout(mainLayout)
        return groupBox

    def signalSlot(self):
        self.bindRbtn.clicked.connect(self.udpLinkStatus)

    def udpConfig(self):
        status = self.udpSocket.bind(int(self.masterPort.text()))
        if status:
            self.udpSocket.readyRead.connect(self.processUDPDatagrams)
        else:
            QMessageBox.warning(self, "警告", 'UDP端口被占用')

    @pyqtSlot(str)
    def sendFrame(self, frame, dataMode='hex', boardCast=False):
        if dataMode == 'utf8':
            data = frame.encode(encoding='utf-8')
        elif dataMode == 'hex':
            data = a2b_hex(frame)
        elif dataMode == 'ascii':
            data = a2b_hex(frame)
        else:
            data = a2b_hex(frame)

        if self.udpSocket.state() == QAbstractSocket.BoundState:
            if boardCast:
                self.udpSocket.writeDatagram(QByteArray(data), QHostAddress.Broadcast,
                                         int(self.targetPort.text()))
            else:
                self.udpSocket.writeDatagram(QByteArray(data), QHostAddress(self.targetIP.text()),
                                             int(self.targetPort.text()))

    @pyqtSlot()
    def processUDPDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            if datagram:
                self.recvDataReady.emit(datagram, host.toString(), port)

    @pyqtSlot()
    def udpLinkStatus(self):
        if self.bindRbtn.isChecked():
            status = self.udpSocket.bind(int(self.masterPort.text()))
            if status:
                self.udpSocket.readyRead.connect(self.processUDPDatagrams)
            else:
                QMessageBox.warning(self, "警告", 'UDP端口被占用')
                self.bindRbtn.setChecked(False)
        else:
            self.udpSocket.disconnectFromHost()

    def currentStatus(self):
        '''
        udp只有BoundState和UnconnectedState
        :return:
        '''
        if self.udpSocket.state() == QAbstractSocket.UnconnectedState:
            return [False, 'socket没有连接']
        elif self.udpSocket.state() == QAbstractSocket.HostLookupState:
            return [False, 'socket正在查找主机名称']
        elif self.udpSocket.state() == QAbstractSocket.ConnectingState:
            return [False, 'socket正在查找主机名称']
        elif self.udpSocket.state() == QAbstractSocket.ConnectedState:
            return [False, '连接已建立']
        elif self.udpSocket.state() == QAbstractSocket.BoundState:
            return [True, 'socket绑定到一个地址和端口']
        elif self.udpSocket.state() == QAbstractSocket.ClosingState:
            return [False, 'socket即将关闭']
        elif self.udpSocket.state() == QAbstractSocket.ConnectedState:
            return [False, '仅限内部使用']

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = UdpCore()
    ui.show()
    sys.exit(app.exec_())
