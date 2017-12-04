#-*- coding:utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.misc.protocol import *


class CommandTest(QWidget):
    packetFrameDone = pyqtSignal([str])
    def __init__(self):
        super(CommandTest, self).__init__()
        self.packet = EncodeProtocol()
        self.commandTable = {
            '查找设备': '00000000',
            '激光透传数据': '00000001',
            '激光频率': '00000002',
            '电机透传数据': '00000003',
            '设置dac': '00000004',
            '读取adc': '00000005',
            'ad采样长度': '00000008',
            'ad预览系数': '00000009',
            '存储文件名': '0000000a',
            '存储使能': '0000000b',
            '采集使能': '0000000c',
            '复位计数器': '00000010',
            '设置备用输出io': '00000011',
            '读取备用输入io': '00000012',
            '读取设备参数': '00000013',
            '固件更新开始': '00000014',
            '固件更新数据': '00000015',
            '固件更新结束': '00000016',
            '系统复位': '00000017',
            '硬盘读取地址': '00000018',
            '硬盘写入地址': '00000019',
            '预览帧数': '00000020',
            'ch0采集长度': '00000021',
            'ch0起始位置': '00000022',
            'ch0有效长度': '00000023',
            'ch1采集长度': '00000024',
            'ch1起始位置': '00000025',
            'ch1和阈值': '00000026',
            'ch1值阈值': '00000027',
            '激光使能': '00000028'
        }

        self.initUI()

        self.sendBtn.clicked.connect(self.configFrame)
    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.commandGroup())
        self.setLayout(mainLayout)

    def commandGroup(self):
        groupBox = QGroupBox('发送命令设置')

        self.commandLabel = QLabel('指令')
        self.dataLabel = QLabel('数据')

        self.commandComb = QComboBox()
        for text in self.commandTable:
            self.commandComb.addItem(text)
        self.dataLine = QLineEdit('00 00 00 01')
        self.sendBtn = QPushButton()
        self.sendBtn.setIcon(QIcon('images/send.svg'))
        self.sendBtn.setIconSize(QSize(64, 32))

        form = QFormLayout()
        form.addRow(self.commandLabel, self.commandComb)
        form.addRow(self.dataLabel, self.dataLine)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addWidget(self.sendBtn)

        groupBox.setLayout(vbox)
        return groupBox

    @pyqtSlot()
    def configFrame(self):
        head = 'AA555AA5 AA555AA5'

        cmd_num = 'bbbbbbbb'

        for text in self.commandTable:
            if text == self.commandComb.currentText():
                command = self.commandTable[text]

        data_len = len(self.commandComb.currentText().replace(' ', ''))
        if data_len <= 8:
            data_len = 4
        else:
            data_len = data_len//2

        data = self.dataLine.text()

        self.packet.config(head=head, cmd_num=cmd_num, command=command, data_len=str(data_len), data=data)
        frame = self.packet.getFrame()
        print(frame)
        self.packetFrameDone.emit(frame)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = CommandTest()
    ui.show()
    sys.exit(app.exec_())
