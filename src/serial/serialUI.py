#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *

from ..serial.extendFunction import *
from ..serial.serialWidget import *

class SerialUI(QMainWindow):
    def __init__(self):
        super(SerialUI, self).__init__()

        self.resize(800, 500)
        self.setWindowTitle('串口调试工具')
        self.setWindowIcon(QIcon('images/serialIcon.svg'))
        self.initUI()

        self.helpWidget = HelpWidget()
        self.helpWidget.hide()

    def initUI(self):
        self.serialInfo = SerialWidget()
        recvSet = self.recvConfigUI()
        sendSet = self.sendConfigUI()
        recvData = self.recvdataUI()
        sendData = self.sendDataUI()
        self.mutilString = MutilString()
        self.protocolFrame = ProtocalFrame()
        # self.extendUI.hide()

        tab = QTabWidget()
        tab.addTab(sendData, '基本数据')
        tab.addTab(self.mutilString, '多字符串')
        tab.addTab(self.protocolFrame, '自定义协议')

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.serialInfo)
        rightLayout.addWidget(recvSet)
        rightLayout.addWidget(sendSet)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(recvData)
        leftLayout.addWidget(tab)
        leftLayout.setStretchFactor(recvData, 3)
        leftLayout.setStretchFactor(tab, 2)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(rightLayout)
        mainLayout.addLayout(leftLayout)
        mainLayout.setStretchFactor(rightLayout, 1)
        mainLayout.setStretchFactor(leftLayout, 3)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def recvConfigUI(self):
        self.hexRecvRbtn = QRadioButton('HEX')
        self.asciiRecvRbtn = QRadioButton('ASCII')
        self.hexRecvRbtn.setChecked(True)

        self.writeDataToFileCb = QCheckBox('接受数据写入文件')
        self.autoWrapCb = QCheckBox('自动换行')
        self.pauseReceiveCb = QCheckBox('暂停接收')
        self.saveRecvBtn = QPushButton('保存数据')
        self.saveRecvBtn.setToolTip('保存当前接受数据区的数据')
        self.clearRecvBtn = QPushButton('清除显示')

        hbox = QHBoxLayout()
        hbox.addWidget(self.asciiRecvRbtn)
        hbox.addWidget(self.hexRecvRbtn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.writeDataToFileCb)
        vbox.addWidget(self.autoWrapCb)
        vbox.addWidget(self.pauseReceiveCb)
        vbox.addWidget(self.saveRecvBtn)
        vbox.addWidget(self.clearRecvBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addLayout(vbox)

        groupBox = QGroupBox('接受设置')
        groupBox.setLayout(mainLayout)
        return groupBox

    def sendConfigUI(self):
        self.hexSendRbtn = QRadioButton('HEX')
        self.asciiSendRbtn = QRadioButton('ASCII')
        self.hexSendRbtn.setChecked(True)

        self.timeSendCb = QCheckBox('定时发送(ms)：')
        self.timeEdit = QLineEdit('1000')

        hbox = QHBoxLayout()
        hbox.addWidget(self.asciiSendRbtn)
        hbox.addWidget(self.hexSendRbtn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.timeSendCb)
        vbox.addWidget(self.timeEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addLayout(vbox)
        groupBox = QGroupBox('发送设置')
        groupBox.setLayout(mainLayout)
        return groupBox

    def recvdataUI(self):
        self.recvText = QTextEdit()
        self.recvText.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.recvText)

        groupBox = QGroupBox('接收数据区')
        groupBox.setLayout(vbox)
        return groupBox

    def sendDataUI(self):
        self.sendEdit = QLineEdit()
        self.sendEdit.setToolTip('HEX模式时，发送的数据不包括空格')
        self.sendEdit.setValidator(QRegExpValidator(QRegExp("[a-fA-F0-9 ]+$")))
        self.loadFileBtn = QPushButton('选择文件')
        self.loadFileEdit = QLineEdit()
        self.loadFileEdit.setReadOnly(True)
        self.sendBtn = QPushButton('发送')
        self.sendFileBtn = QPushButton('发送文件')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.loadFileBtn)
        hbox1.addWidget(self.loadFileEdit)
        hbox1.addWidget(self.sendFileBtn)

        vbox = QHBoxLayout()
        vbox.addWidget(self.sendEdit)
        vbox.addWidget(self.sendBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(vbox)
        mainLayout.addLayout(hbox1)

        frame = QFrame()
        frame.setLayout(mainLayout)
        return frame

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = SerialUI()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())
