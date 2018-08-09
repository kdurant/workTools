
#-*- coding:utf-8 -*-
from binascii import a2b_hex

from PyQt5.QtCore import *
from PyQt5.QtSerialPort import *
from PyQt5.QtWidgets import *

from src.common.protocol import *


class GpsTest(QWidget):
    packetFrameDone = pyqtSignal([str])
    dataReady = pyqtSignal(bytes)

    def __init__(self):
        super(GpsTest, self).__init__()
        self.packet = EncodeProtocol()
        self.com = QSerialPort()

        self.data = 'aa550359074864c61900dabf42684ecec18267b840d576ce0d0a7eac584138f907000000000000000000b1d3a1421023aac1ec07f2c00000000000130cd5'

        self.initUI()

        self.com.readyRead.connect(self.recvData)
        self.openBtn.clicked.connect(self.openCom)
        self.closeBtn.clicked.connect(self.closeCom)
        self.dataReady[bytes].connect(self.sendData)
        self.startTestBtn.clicked.connect(self.generateSerialData)
        self.detectSerialStatus()


    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.serialConfigUI())
        vbox.addWidget(self.gpsTestUI())

        self.setLayout(vbox)

    def serialConfigUI(self):
        self.serialPortComb = QComboBox()
        self.openBtn = QPushButton('打开串口')
        self.closeBtn = QPushButton('关闭串口')

        hbox = QHBoxLayout()
        hbox.addWidget(self.serialPortComb)
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.closeBtn)

        hbox.addStretch(1)

        group = QGroupBox()
        group.setLayout(hbox)
        return group

    def gpsTestUI(self):
        self.startTestBtn = QPushButton('开始测试')
        self.resultLabel = QLabel('测试结果:')
        self.resultLine = QLineEdit()
        self.resultLine.setReadOnly(True)

        self.label = QLabel()
        self.label.setText(
                            '<font size=14 color="#FF0000">说明：</font> <br />'
                           '1. 将PC串口pin3（PC发送数据引脚)连到到扩展板GPS串口J1.3 <br />'
                           # '2. 将PC串口pin2（PC接受数据引脚)连接到扩展板GPS串口J1.1 <br />'
                           '3. 打开串口 <br />'
                           '4. 点击开始测试按钮<br />'
                           '5. 查看测试结果<br />'

        )

        hbox = QHBoxLayout()
        hbox.addWidget(self.resultLabel)
        hbox.addWidget(self.resultLine)
        hbox.addWidget(self.startTestBtn)
        hbox.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.label)
        mainLayout.addStretch(1)

        group = QGroupBox('GPS串口测试')
        group.setLayout(mainLayout)
        return group

    def detectSerialStatus(self):
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            # if not port.isBusy():
            self.serialPortComb.addItem(port.portName())

    def generateSerialData(self):
        data = a2b_hex(self.data)
        self.dataReady.emit(data)

        pass

    def recvData(self):
        '''
        当以非HEX方式发送数据时：
        发送 '12' : 收到的是 b'1', b'2'
        发送 '中文' : 收到的是 b'\xe4\xb8\xad', b'\xe6\x96\x87'
        可得出结论，发送数据为 s.encode('utf')
        接收到数据时，recv_s.decode('utf8')即可正确显示

        当以HEX方式发送数据时：
        发送 'ab' : 收到 b'\xab'
        :return:
        '''

        recvData = bytes(self.com.readAll())
        print(recvData)

    @pyqtSlot()
    def openCom(self):
        comName = self.serialPortComb.currentText()
        self.com.setPortName(comName)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critecla(self, '打开失败', '该串口不存在或已被占用')
                return
            else:
                self.openBtn.setEnabled(False)
                self.closeBtn.setEnabled(True)
        except:
            QMessageBox.critical(self, '打开失败', '该串口不存在或已被占用')
            return
        self.com.setBaudRate(115200)
        self.com.setDataBits(8)
        self.com.setStopBits(1)

    @pyqtSlot()
    def closeCom(self):
        if self.com.isOpen():
            self.com.close()
            self.openBtn.setEnabled(True)
            self.closeBtn.setEnabled(False)
            return

    @pyqtSlot(bytes)
    def sendData(self, data):
        '''
        ascii 方式发送 '34', HEX显示为 '33 34'; ascii显示为 '34'
        hex 方式发送 '34', HEX显示为 '34'; ascii显示为 '4'
        :return:
        '''

        if self.openBtn.isEnabled():
            QMessageBox.warning(self, '警告', '请先打开串口')
            return

        n = self.com.write(data)

    @pyqtSlot(str)
    def processFrame(self, frame):
        length = int(frame[40:48], 16) + 1
        data = frame[48:48+length*2]

        if data == self.data:
            self.resultLine.setText('测试通过')
        else:
            self.resultLine.setText('测试失败')