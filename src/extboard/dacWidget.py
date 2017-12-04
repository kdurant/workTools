#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.common.protocol import *


class dacWidget(QWidget):
    packetFrameDone= pyqtSignal([str])
    def __init__(self):
        super(dacWidget, self).__init__()
        self.packet = EncodeProtocol()
        self.chSelectComb = QComboBox()
        self.chSelectComb.addItems(['APD HV', 'PMT1', 'PMT2', 'PMT3'])
        self.chDigtalValue = QComboBox()
        self.chDigtalValue.addItems(['0', '500', '1000', '1500', '2000', '2500', '3000', '3500', '4000'])
        self.nextBtn = QPushButton('下一个')
        self.setBtn = QPushButton('设置')
        self.label = QLabel()

        self.label.setText(
                            '<font size=14 color="#FF0000">说明：</font> <br />'
                            'APD HV对应扩展板DAC通道0， 端口是APD.pin7<br />' 
                            'PMT1对应扩展板DAC通道1， 端口是PMT1.pin1<br />'
                            'PMT2对应扩展板DAC通道2， 端口是PMT2.pin1<br />'
                            'PMT3对应扩展板DAC通道3， 端口是PMT3.pin1<br />'
                            '<br />'
                            '每个DAC通道设置9个数字值，记录对应输出模拟值，得到实际的拟合曲线，提供给上位机<br /> '
                            '<font size=12 color="#D2691E">注意：</font> <br />'
                            '每设置一个APD HV值，需要记录U8.15的模拟电压值，然后去ADC测试页面读取APD FB的值'
                           )

        hbox = QHBoxLayout()
        hbox.addWidget(self.chSelectComb)
        hbox.addWidget(self.chDigtalValue)
        hbox.addWidget(self.nextBtn)
        hbox.addWidget(self.setBtn)
        hbox.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addLayout(hbox)
        mainLayout.addStretch(1)
        mainLayout.addWidget(self.label)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

        self.setBtn.clicked.connect(self.configFrame)
        self.nextBtn.clicked.connect(self.changeValue)

    @pyqtSlot()
    def changeValue(self):
        index = self.chDigtalValue.currentIndex()
        index += 1
        if index == self.chDigtalValue.count():
            index = 0
        self.chDigtalValue.setCurrentIndex(index)
    @pyqtSlot()
    def configFrame(self):
        head = 'AA555AA5 AA555AA5'
        cmd_num = 'ddaaccdd'
        command = '00000004'
        # pck_num = '1'
        data_len = '8'

        if self.chSelectComb.currentText() == 'APD HV':
            data_front = '0000 0000'
        elif self.chSelectComb.currentText() == 'PMT1':
            data_front = '0000 0001'
        elif self.chSelectComb.currentText() == 'PMT2':
            data_front = '0000 0002'
        elif self.chSelectComb.currentText() == 'PMT3':
            data_front = '0000 0003'

        data_back = str(hex(int(self.chDigtalValue.currentText(), 10))).replace('0x', '').zfill(8)

        data = data_front + data_back

        self.packet.config(head=head, cmd_num=cmd_num, command=command, data_len=data_len, data=data)
        frame = self.packet.getFrame()
        self.packetFrameDone.emit(frame)
