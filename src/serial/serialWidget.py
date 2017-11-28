#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *
from binascii import a2b_hex, b2a_hex


class SerialWidget(QWidget):
    serialDataReady = pyqtSignal(bytes)
    serialStateChanged = pyqtSignal(bool)
    def __init__(self):
        super(SerialWidget, self).__init__()
        self.com = QSerialPort()
        self.sendCnt = 0
        self.recvCnt = 0
        self.serialStatus = False

        self.initUI()
        self.detectSerialStatus()
        self.signalSlot()

    def initUI(self):
        serialInfo = self.serialParaUI()

        vbox = QVBoxLayout()
        vbox.addWidget(serialInfo)
        self.setLayout(vbox)

    def serialParaUI(self):
        self.serialNumComb = QComboBox()
        self.serialBaudComb = QComboBox()
        self.serialBaudComb.addItems(['9600', '14400', '38400', '56000', '57600', '115200', '128000'])
        self.serialBaudComb.setCurrentText('115200')
        self.serialCheckComb = QComboBox()
        self.serialCheckComb.addItems(['None'])
        self.serialDataLenComb = QComboBox()
        self.serialDataLenComb.addItems(['5', '6', '7', '8'])
        self.serialDataLenComb.setCurrentText('8')
        self.serialStopComb = QComboBox()
        self.serialStopComb.addItems(['1', '2'])
        self.openBtn = QPushButton('打开串口')
        self.openBtn.setObjectName('openBtn')

        self.closeBtn = QPushButton('关闭串口')
        self.closeBtn.setEnabled(False)

        formLayout = QFormLayout()
        formLayout.addRow('串口号：', self.serialNumComb)
        formLayout.addRow('波特率：', self.serialBaudComb)
        formLayout.addRow('校验位：', self.serialCheckComb)
        formLayout.addRow('数据位：', self.serialDataLenComb)
        formLayout.addRow('停止位：', self.serialStopComb)

        hbox = QHBoxLayout()
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.closeBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(hbox)

        groupBox = QGroupBox('串口设置')
        groupBox.setLayout(mainLayout)

        return groupBox

    def detectSerialStatus(self):
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            # if not port.isBusy():
            self.serialNumComb.addItem(port.portName())

    def signalSlot(self):
        self.openBtn.clicked.connect(self.openCom)
        self.closeBtn.clicked.connect(self.closeCom)
        self.com.readyRead.connect(self.recvData)

    @pyqtSlot()
    def openCom(self):
        comName = self.serialNumComb.currentText()
        self.com.setPortName(comName)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critecla(self, '打开失败', '该串口不存在或已被占用')
                return
            else:
                self.openBtn.setEnabled(False)
                self.closeBtn.setEnabled(True)
                self.serialStatus = True
                self.serialStateChanged.emit(self.serialStatus)
        except:
            QMessageBox.critical(self, '打开失败', '该串口不存在或已被占用')
            return
        self.com.setBaudRate(int(self.serialBaudComb.currentText()))
        self.com.setDataBits(int(self.serialDataLenComb.currentText()))
        self.com.setStopBits(int(self.serialStopComb.currentText()))

        self.serialNumComb.setEnabled(False)
        self.serialBaudComb.setEnabled(False)
        self.serialCheckComb.setEnabled(False)
        self.serialDataLenComb.setEnabled(False)
        self.serialStopComb.setEnabled(False)

    @pyqtSlot()
    def closeCom(self):
        if self.com.isOpen():
            self.com.close()
            self.openBtn.setEnabled(True)
            self.closeBtn.setEnabled(False)
            self.sendCnt = 0
            self.recvCnt = 0
            self.serialStatus = False
            self.serialStateChanged.emit(self.serialStatus)

            self.serialNumComb.setEnabled(True)
            self.serialBaudComb.setEnabled(True)
            self.serialCheckComb.setEnabled(True)
            self.serialDataLenComb.setEnabled(True)
            self.serialStopComb.setEnabled(True)
            return

    @pyqtSlot(str, bool)
    def sendData(self, data, sendMode=True):
        '''
        :param data: 需要发送的数据
        :param sendMode: True，HEX模式发送; False, ASCII模式发送
        :return:

        '12', HEX模式发送：b'\x12', 收到：b'\x12'
              ASCII模式发送：b'12', 收到：b'12'
        '''
        '''
        ascii 方式发送 '34', HEX显示为 '33 34'; ascii显示为 '34'
        hex 方式发送 '34', HEX显示为 '34'; ascii显示为 '4'
        :return:
        '''

        if self.openBtn.isEnabled():
            QMessageBox.warning(self, '警告', '请先打开串口')
            return
        if sendMode:
            data = data.replace(' ', '')
            if len(data) % 2 == 0:
                try:
                    data = a2b_hex(data)
                except ValueError:
                    QMessageBox.critical(self, '警告', 'HEX模式不能发送非ASCII字符')
                    return
            else:
                QMessageBox.warning(self, '警告', '十六进制数不是偶数个')
                return
        else:
            data = data.encode('utf8')

        n = self.com.write(data)
        self.sendCnt += n

    @pyqtSlot()
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
        try:
            # recvData = bytes(self.com.readAll())
            recvData = bytes(self.com.read(65535))
            self.recvCnt += len(recvData)
            self.serialDataReady.emit(recvData)
        except:
            pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = SerialWidget()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())