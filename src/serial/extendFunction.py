#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from binascii import a2b_hex, b2a_hex

class MutilString(QWidget):
    '''
    可设置发送多条字符串
    '''
    dataReady = pyqtSignal(str, bool)
    def __init__(self):
        super(MutilString, self).__init__()
        self.selCbList = []
        self.hexEditList = []
        self.sendBtnList = []

        self.timer = QTimer()
        self.initUI()
        self.signalSlot()

    def initUI(self):
        t = self.mutlUI()
        vbox = QHBoxLayout()
        vbox.addWidget(t)
        self.setLayout(vbox)

    def mutlUI(self):
        grid = QGridLayout()
        for i in range(0, 8):
            self.selCbList.append(QCheckBox())
            self.hexEditList.append(QLineEdit())
            self.hexEditList[i].setValidator(QRegExpValidator(QRegExp("[a-fA-F0-9 ]+$")))
            btn = QPushButton(str(i))
            btn.setFixedWidth(30)
            self.sendBtnList.append(btn)
            self.sendBtnList[i].clicked.connect(self.sendSingleStr)
            row = i + 1
            grid.addWidget(self.selCbList[i], row, 0)
            grid.addWidget(self.hexEditList[i], row, 1)
            grid.addWidget(self.sendBtnList[i], row, 2)

        selLabel = QLabel('选择')
        strLabel = QLabel('字符串')
        sendLabel = QLabel('发送')

        grid.addWidget(selLabel, 0, 0)
        grid.addWidget(strLabel, 0, 1)
        grid.addWidget(sendLabel, 0, 2)
        grid.setAlignment(Qt.AlignHCenter)


        self.cycleSendCb = QCheckBox('循环发送')
        self.hexSendCb = QCheckBox('hex发送')
        self.hexSendCb.setChecked(True)

        hbox = QHBoxLayout()
        hbox.addWidget(self.cycleSendCb)
        hbox.addWidget(self.hexSendCb)

        self.cycleInterTimeEdit = QLineEdit('1000')
        self.cycleInterTimeEdit.setToolTip('所有字符串发次一次时间间隔')
        self.strInterTimeEdit = QLineEdit('50')
        self.strInterTimeEdit.setToolTip('每条字符串时间间隔')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.cycleSendCb)
        hbox1.addWidget(self.hexSendCb)
        hbox1.addWidget(QLabel('周期(ms)：'))
        hbox1.addWidget(self.cycleInterTimeEdit)
        hbox1.addWidget(QLabel('间隔时间(ms)：'))
        hbox1.addWidget(self.strInterTimeEdit)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        # vbox.addLayout(hbox)
        vbox.addLayout(grid)
        vbox.addStretch()

        # self.setLayout(vbox)

        frame = QFrame()
        frame.setLayout(vbox)

        s = QScrollArea()
        s.setWidget(frame)
        s.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        s.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        s.setWidgetResizable(True)
        return s

    def signalSlot(self):
        self.cycleSendCb.stateChanged.connect(self. startCycleTime)
        self.timer.timeout.connect(self.prepareData)
        pass
    @pyqtSlot()
    def startCycleTime(self):
        if self.cycleSendCb.isChecked():
            self.timer.start(int(self.cycleInterTimeEdit.text()))
        else:
            self.timer.stop()

    @pyqtSlot()
    def prepareData(self):
        for i in range(0, 8):
            if self.selCbList[i].isChecked():
                data = self.hexEditList[i].text()
                self.dataReady.emit(data, True)
                QThread.msleep(int(self.strInterTimeEdit.text()))
        pass

    def sendSingleStr(self):
        sender = self.sender()
        num = int(sender.text())
        data = self.hexEditList[num].text()
        if data:
            if self.hexSendCb.isChecked():
                self.dataReady.emit(data, True)
            else:
                self.dataReady.emit(data, False)
        else:
            QMessageBox.warning(self, '警告', '发送内容不能为空')

class ProtocalFrame(QFrame):
    dataReady = pyqtSignal(str, bool)
    def __init__(self):
        super(ProtocalFrame, self).__init__()
        self.initUI()
        self.sendProtocalBtn.clicked.connect(self.prepareData)

    def initUI(self):
        self.hexModeRbtn = QRadioButton('HEX')
        self.hexModeRbtn.setChecked(True)
        self.asciiModeRbtn = QRadioButton('ASCII')
        self.sendProtocalBtn = QPushButton('发送')
        self.selectCheckComb = QComboBox()
        self.selectCheckComb.addItems(['异或', '累加和', 'CRC8', 'CRC16'])

        self.table = QTableWidget(3, 8)
        self.table.setHorizontalHeaderLabels(['Field1', '2', '3', '4'])
        self.table.setVerticalHeaderLabels(['长度(Byte)', '数据', '有效'])

        for i in range(self.table.rowCount()):
            if i == 0:
                for j in range(self.table.columnCount()):
                    item = QTableWidgetItem()
                    item.setText('1')
                    self.table.setItem(i, j, item)
            elif i == 2:
                for j in range(self.table.columnCount()):
                    item = QTableWidgetItem('Y')
                    self.table.setItem(i, j, item)
            else:
                pass

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.hexModeRbtn)
        hbox.addWidget(self.asciiModeRbtn)
        hbox.addWidget(QLabel('校验公式：'))
        hbox.addWidget(self.selectCheckComb)
        hbox.addWidget(self.sendProtocalBtn)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)
        pass

    @pyqtSlot()
    def prepareData(self):
        data = ''
        for i in range(self.table.columnCount()):
            if self.table.item(2, i).text() == 'Y':
                tmp = self.table.item(1, i)
                # if tmp == 'None': # 单元格里没有内容
                if tmp is None: # 单元格里没有内容
                    QMessageBox.warning(self, '警告', '选择有效但没有数据')
                    return
                else:
                    len = int(self.table.item(0, i).text())
                    data += self.table.item(1, i).text().zfill(len*2)

        data += self.checkSum(data)
        self.dataReady.emit(data, True)


    def checkSum(self, data):
        checksum = 0
        l = [int(data[x:x + 2], 16) for x in range(0, len(data), 2)]
        if self.selectCheckComb.currentText() == '累加和':
            return ''
        elif self.selectCheckComb.currentText() == '异或':
            for i in l:
                checksum ^= i
            end = str(hex(checksum)).replace('0x', '')
            return end
        elif self.selectCheckComb.currentText() == 'CRC8':
            return ''
        elif self.selectCheckComb.currentText() == 'CRC16':
            return ''

class ExtendFunction(QWidget):
    def __init__(self):
        super(ExtendFunction, self).__init__()

        # mutilString = MutilString()
        protocal = ProtocalFrame()
        vbox = QVBoxLayout()
        vbox.addWidget(protocal)

        self.setLayout(vbox)

class HelpWidget(QWidget):
    def __init__(self):
        super(HelpWidget, self).__init__()
        self.initUI()
        self.setWindowTitle('串口相关信息')

    def initUI(self):
        tab = QTabWidget()
        tab.addTab(self.basicInfoUI(), '基本信息')
        tab.addTab(self.asciiTableUI(), 'ascii码表')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tab)
        self.setLayout(mainLayout)

    def basicInfoUI(self):
        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap('/images/level.png'))
        # self.imageLabel.setPixmap(QPixmap('images/level.png').scaled(QSize(960*0.7, 300*0.8)))  # 缩放label里的图片
        levelInfoLabel = QLabel()
        levelInfoLabel.setText(
                                    '1. USB转串口输出电平：正负5V\n'
                                    '2. MAX232芯片输出电平：正负5V\n'

        )
        timeInfoLabel = QLabel()
        timeInfoLabel.setText(
                                    '1. 波特率9600：0.104ms/bit, 1.04ms/Byte\n'
                                    '2. 波特率38400：0.026ms/bit, 0.26ms/Byte\n'
                                    '3. 波特率115200：8.68us/bit, 86.8us/Byte\n'
        )

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(imageLabel)
        mainLayout.addWidget(levelInfoLabel)
        mainLayout.addWidget(timeInfoLabel)

        frame = QFrame()
        frame.setLayout(mainLayout)
        return frame

    def asciiTableUI(self):
        asciiLabel = QLabel()
        asciiLabel.setPixmap(QPixmap('images/ascii.png'))
        # asciiLabel.setPixmap(QPixmap('images/ascii.png').scaled(QSize(1280*0.7, 851*0.7)))  # 缩放label里的图片

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(asciiLabel)
        frame = QFrame()
        frame.setLayout(mainLayout)

        s = QScrollArea(self)
        s.setWidget(frame)
        s.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        s.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        s.setWidgetResizable(True)
        return s

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = HelpWidget()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())
