#-*- coding:utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .protocol import *
from binascii import a2b_hex, b2a_hex

class adcWidget(QWidget):
    packetFrameDone = pyqtSignal([str])
    def __init__(self):
        super(adcWidget, self).__init__()
        self.count = 0
        self.totalValue = 0
        self.packet = EncodeProtocol()

        self.chSelectComb = QComboBox()
        self.chSelectComb.addItems(['APD TEMP', 'APD FB', 'PMT1', 'PMT2', 'PMT3'])
        self.readVauleBtn = QPushButton('读取')

        self.arvDataEdit = QLineEdit('0')
        self.calcValueEdit = QLineEdit()

        self.data0Edit = QLineEdit()
        self.data1Edit = QLineEdit()
        self.data2Edit = QLineEdit()
        self.data3Edit = QLineEdit()
        self.data4Edit = QLineEdit()

        self.label = QLabel()
        self.label.setText(
                            '<font size=14 color="#FF0000">说明：</font> <br />'
                            'APD TEMP对应扩展板ADC通道0， 端口是APD.pin1 <br />' 
                            'APD FB对应扩展板ADC通道1 <br />'
                            'PMT1对应扩展板ADC通道2， 端口是PMT1.pin5 <br />'
                            'PMT2对应扩展板ADC通道3， 端口是PMT2.pin5 <br />'
                            'PMT3对应扩展板ADC通道4， 端口是PMT3.pin5 <br />'
                            '<br />'
                            'ADC对应端口连接直流电源。直流电源依次设置0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 读取得到的数字值<br />'
                            '<font size=4 color="#FF0000">APD FB不需要接直流电源，在DAC测试设置APD HV时直接读取</font> <br />'
                            '记录模拟值和数字值，得到拟合曲线，提供给上位机'
        )

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('平均值(DEC)：'))
        hbox.addWidget(self.arvDataEdit)
        hbox.addWidget(QLabel('理论计算模拟值：'))
        hbox.addWidget(self.calcValueEdit)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.chSelectComb)
        hbox1.addWidget(self.readVauleBtn)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel('data0: '))
        hbox2.addWidget(self.data0Edit)

        hbox2.addWidget(QLabel('data1: '))
        hbox2.addWidget(self.data1Edit)

        hbox2.addWidget(QLabel('data2: '))
        hbox2.addWidget(self.data2Edit)

        hbox2.addWidget(QLabel('data3: '))
        hbox2.addWidget(self.data3Edit)

        hbox2.addWidget(QLabel('data4: '))
        hbox2.addWidget(self.data4Edit)
        # hbox2.addRow('data4:', self.data4Edit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox1)
        mainLayout.addLayout(hbox)
        mainLayout.addLayout(hbox2)

        mainLayout.addWidget(self.label)

        self.setLayout(mainLayout)
        self.readVauleBtn.clicked.connect(self.configFrame)

    @pyqtSlot()
    def configFrame(self):
        head = 'AA555AA5 AA555AA5'
        cmd_num = 'aaddccaa'
        command = '00000005'
        # pck_num = '1'
        data_len = '4'

        if self.chSelectComb.currentText() == 'APD TEMP':
            data = '0000 0000'
        elif self.chSelectComb.currentText() == 'APD FB':
            data = '0000 0001'
        elif self.chSelectComb.currentText() == 'PMT1':
            data = '0000 0002'
        elif self.chSelectComb.currentText() == 'PMT2':
            data = '0000 0003'
        elif self.chSelectComb.currentText() == 'PMT3':
            data = '0000 0004'


        self.packet.config(head=head, cmd_num=cmd_num, command=command, data_len=data_len, data=data)
        frame = self.packet.getFrame()
        for i in range(0, 5):
            self.packetFrameDone.emit(frame)
            QThread.msleep(20)

    @pyqtSlot(str)
    def processFrame(self, frame):
        self.count += 1
        data = frame[56:64]
        data = int(data, 16)
        self.totalValue += data

        if self.count == 1:
            self.data0Edit.setText(str(data))
        elif self.count == 2:
            self.data1Edit.setText(str(data))
        elif self.count == 3:
            self.data2Edit.setText(str(data))
        elif self.count == 4:
            self.data3Edit.setText(str(data))
        elif self.count == 5:
            self.data4Edit.setText(str(data))
            self.count = 0
            arvValue = self.totalValue // 5
            self.arvDataEdit.setText(str(arvValue))
            self.totalValue = 0
