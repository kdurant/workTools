#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.misc.protocol import *


class LaserTest(QWidget):
    packetFrameDone = pyqtSignal([str])
    generateDataDone = pyqtSignal(str, str, str)
    def __init__(self):
        super(LaserTest, self).__init__()
        self.packet = EncodeProtocol()

        self.initUI()
        self.serialTestBtn.clicked.connect(self.generateSerialData)
        self.serialTestBtn.clicked.connect(self.resultLine.clear)
        self.openLaserBtn.clicked.connect(self.generateOpenData)
        self.closeLaserBtn.clicked.connect(self.generateCloseData)
        self.freqTestBtn.clicked.connect(self.generateFreqData)
        self.generateDataDone[str, str, str].connect(self.configFrame)

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.switchTestUI())
        hbox.addWidget(self.freqTestUI())

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.serialTestUI())
        self.setLayout(mainLayout)

    def serialTestUI(self):
        self.inputDataLabel = QLabel('输入测试数据：')
        self.downLoadDataLine = QLineEdit()
        self.downLoadDataLine.setValidator(QRegExpValidator(QRegExp("[a-fA-F0-9 ]+$")))

        self.serialTestBtn = QPushButton('开始测试')
        self.resultLabel = QLabel('测试结果:')
        self.resultLine = QLineEdit()
        self.resultLine.setReadOnly(True)

        self.info = QLabel()

        self.info.setText(
                            '<font size=4 color="#FF0000">说明：</font> <br />'
                            '1. 短接扩展板激光串口输入输出端(J2.2, J2.4)(由J3.1，J3.3调整到此)<br />'
                            '2. 输入测试数据<br />'
                            '3. 点击开始测试按钮，观察下方测试结果<br />'
                          )

        grid = QGridLayout()
        grid.addWidget(self.inputDataLabel, 0, 0)
        grid.addWidget(self.downLoadDataLine, 0, 1)
        grid.addWidget(self.serialTestBtn, 1, 0)
        grid.addWidget(self.resultLabel, 0, 2)
        grid.addWidget(self.resultLine, 0, 3)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(grid)
        mainLayout.addWidget(self.info)

        mainLayout.addStretch(1)
        group = QGroupBox('串口通信测试')

        group.setLayout(mainLayout)
        return group

    def switchTestUI(self):
        self.openLaserBtn = QPushButton('打开激光器')
        self.closeLaserBtn = QPushButton('关闭激光器')
        self.switchinfoLabel = QLabel()
        self.switchinfoLabel.setText(
                                    '<font size=4 color="#FF0000">说明：</font> (开关测试引脚：J3.2) <br />'
                                     '打开，采集卡输出电平1(3.3V), 扩展板输出电平0(0V)<br />'
                                     '关闭，采集卡输出电平0(0V), 扩展板输出电平1(5V)<br />'
                                     )

        hbox = QHBoxLayout()
        hbox.addWidget(self.openLaserBtn)
        hbox.addWidget(self.closeLaserBtn)
        hbox.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.switchinfoLabel)
        group = QGroupBox('开关测试')
        group.setLayout(mainLayout)

        return group

    def freqTestUI(self):
        self.freqLabel = QLabel('输入频率Hz: ')
        self.freqLine = QLineEdit('5000')
        self.freqTestBtn = QPushButton('设置频率')
        self.freqInfoLabel = QLabel()
        self.freqInfoLabel.setText(
                                    '<font size=4 color="#FF0000">说明：</font>'
                                    '频率测试引脚：J3.4'
                                   )

        form = QFormLayout()

        form.addRow(self.freqLabel, self.freqLine)
        form.addWidget(self.freqTestBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(form)

        mainLayout.addWidget(self.freqInfoLabel)

        # mainLayout = QVBoxLayout()
        # mainLayout.addLayout(form)
        group = QGroupBox('频率测试')
        group.setLayout(mainLayout)
        return group

    @pyqtSlot()
    def generateSerialData(self):
        command = '00000001'
        data = self.downLoadDataLine.text()
        length = int(len(data) / 2)
        data = data[:length*2]


        length = str(int(len(data) / 2))

        if not self.downLoadDataLine.text():
            QMessageBox.warning(self, '警告', '没有输入数据')
            return
        self.generateDataDone.emit(command, length, data)

    @pyqtSlot()
    def generateOpenData(self):
        command = '00000028'
        length = '4'
        data = '00000001'
        self.generateDataDone.emit(command, length, data)

    @pyqtSlot()
    def generateCloseData(self):
        command = '00000028'
        length = '4'
        data = '00000000'
        self.generateDataDone.emit(command, length, data)

    @pyqtSlot()
    def generateFreqData(self):
        command = '00000002'
        length = '4'
        data = self.freqLine.text()
        data = str(hex(int(data)))[2:]
        if not self.freqLine.text():
            QMessageBox.warning(self, '警告', '没有输入数据')
            return
        self.generateDataDone.emit(command, length, data)

    @pyqtSlot(str, str, str)
    def configFrame(self, command, length, data):
        head = 'AA555AA5 AA555AA5'

        cmd_num = 'bbbbbbbb'
        command = command
        data_len = length
        data = data

        self.packet.config(head=head, cmd_num=cmd_num, command=command, data_len=data_len, data=data)
        frame = self.packet.getFrame()
        self.packetFrameDone.emit(frame)

    def processFrame(self, frame):
        length = int(frame[40:48])
        data = frame[48:48+length*2]

        if data == self.downLoadDataLine.text()[:length*2]:
            self.resultLine.setText('测试通过')
            QMessageBox.information(self, '结果', '测试通过')
        else:
            self.resultLine.setText('测试失败')
            QMessageBox.information(self, '结果', '测试失败')