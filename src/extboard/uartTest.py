#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.common.protocol import *


class UartTest(QWidget):
    packetFrameDone = pyqtSignal([str])
    def __init__(self, str):
        super(UartTest, self).__init__()
        self.testType = str
        self.packet = EncodeProtocol()

        self.initUI()
        self.startTestBtn.clicked.connect(self.generateData)
        self.startTestBtn.clicked.connect(self.resultLine.clear)

    def initUI(self):
        self.inputDataLabel = QLabel('输入测试数据：')
        self.inputDataLine = QLineEdit()
        self.inputDataLine.setValidator(QRegExpValidator(QRegExp("[a-fA-F0-9 ]+$")))

        self.startTestBtn = QPushButton('串口通信测试')
        self.resultLabel = QLabel('测试结果:')
        self.resultLine = QLineEdit()
        self.resultLine.setReadOnly(True)

        self.info = QLabel()
        if self.testType == 'motor':
            self.info.setText('说明:\n'
                               '1. 短接扩展板电机串口输入输出端(J2.1, J2.3)\n'
                               '2. 输入测试数据\n'
                               '3. 点击开始测试按钮，观察下方测试结果\n'
                              )
        else:
            self.info.setText('说明:\n'
                               '1. 短接扩展板激光串口输入输出端(J3.1, J3.3)\n'
                               '2. 输入测试数据\n'
                               '3. 点击开始测试按钮，观察下方测试结果\n'
                              )

        grid = QGridLayout()
        grid.addWidget(self.inputDataLabel, 0, 0)
        grid.addWidget(self.inputDataLine, 0, 1)
        grid.addWidget(self.startTestBtn, 1, 0)
        grid.addWidget(self.resultLabel, 2, 0)
        grid.addWidget(self.resultLine, 2, 1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(grid)
        mainLayout.addWidget(self.info)

        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

    @pyqtSlot()
    def generateData(self):
        head = 'AA555AA5 AA555AA5'

        if self.testType == 'motor':
            cmd_num = 'aaaaaaaa'
            command = '00000003'
        elif self.testType == 'laser':
            cmd_num = 'bbbbbbbb'
            command = '00000001'
        # pck_num = '1'
        if not self.inputDataLine.text():
            QMessageBox.warning(self, '警告', '没有输入数据')
            return
        length = int(len(self.inputDataLine.text()) / 2)
        data_len = str(length)
        data = self.inputDataLine.text()[:length * 2]

        self.packet.config(head=head, cmd_num=cmd_num, command=command, data_len=data_len, data=data)
        frame = self.packet.getFrame()
        self.packetFrameDone.emit(frame)

    def processFrame(self, frame):
        length = int(frame[40:48])
        data = frame[48:48+length*2]

        if data == self.inputDataLine.text()[:length*2]:
            self.resultLine.setText('测试通过')
            QMessageBox.information(self, '结果', '测试通过')
        else:
            self.resultLine.setText('测试失败')
            QMessageBox.information(self, '结果', '测试失败')