from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
import sys

from binascii import a2b_hex, b2a_hex
from src import *

import queue

class DataAnalyze(QObject):
    data_analyze_done = pyqtSignal(list)
    def __init__(self, queue, frame):
        super(DataAnalyze, self).__init__()
        self.q = queue
        self.frame = frame

    def start(self, startFlag = False):
        self.startFlag = startFlag

    def stop(self, stopFlag = False):
        self.startFlag = stopFlag

    def work(self):
        while self.startFlag:
            if not self.q.empty():
                data = self.q.get()
                self.frame.config(data)
                if self.frame.analyzeFrame() == True:
                    self.data_analyze_done.emit(self.q.put())


class CaptureBoard(QWidget):
    # data_analyze_start = pyqtSignal()
    packetFrameDone = pyqtSignal([str])
    def __init__(self):
        super(CaptureBoard, self).__init__()
        self.resize(QSize(1200, 600))

        self.frame = ''

        self.udpTxPck = EncodeProtocol()
        self.udpRxPck = DecodeProtocol()
        self.waveQueue = queue.Queue(-1)

        self.initUI()
        self.signalSlot()
        self.threadConfig()

    def threadConfig(self):
        self.analyze = DataAnalyze(self.waveQueue, self.udpRxPck)
        self.analyzeThread = QThread()
        self.analyze.moveToThread(self.analyzeThread)
        self.analyzeThread.started.connect(self.analyze.work)
        self.analyze.data_analyze_done[list].connect(self.updateChart)

    def initUI(self):
        self.udpCore = UdpCore()
        self.startBtn = QPushButton('开始采集')
        self.stopBtn = QPushButton('停止采集')
        self.dataCheck = self.previewDataUI()
        self.chart = Chart()
        hbox = QVBoxLayout()
        hbox.addWidget(self.udpCore)
        hbox.addWidget(self.startBtn)
        hbox.addWidget(self.stopBtn)
        # hbox.addWidget(self.dataCheck)


        leftLayout = QVBoxLayout()
        leftLayout.addLayout(hbox)
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.dataCheck)
        rightLayout.addWidget(self.chart)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        mainLayout.setStretchFactor(leftLayout, 1)
        mainLayout.setStretchFactor(rightLayout, 2)

        self.setLayout(mainLayout)

    def previewDataUI(self):
        frame = QFrame()
        self.ch0_max_label = QLabel('ch0 max:')
        self.ch1_max_label = QLabel('ch1 max:')
        self.ch2_max_label = QLabel('ch2 max:')
        self.ch3_max_label = QLabel('ch3 max:')
        self.ch0_max_value = QLineEdit()
        self.ch1_max_value = QLineEdit()
        self.ch2_max_value = QLineEdit()
        self.ch3_max_value = QLineEdit()
        self.ch0_min_label = QLabel('ch0 min:')
        self.ch1_min_label = QLabel('ch1 min:')
        self.ch2_min_label = QLabel('ch2 min:')
        self.ch3_min_label = QLabel('ch3 min:')
        self.ch0_min_value = QLineEdit()
        self.ch1_min_value = QLineEdit()
        self.ch2_min_value = QLineEdit()
        self.ch3_min_value = QLineEdit()
        self.ch0_diff_label = QLabel('ch0 f-f:')
        self.ch1_diff_label = QLabel('ch1 f-f:')
        self.ch2_diff_label = QLabel('ch2 f-f:')
        self.ch3_diff_label = QLabel('ch3 f-f:')
        self.ch0_diff_value = QLineEdit()
        self.ch1_diff_value = QLineEdit()
        self.ch2_diff_value = QLineEdit()
        self.ch3_diff_value = QLineEdit()

        grid = QGridLayout()
        grid.addWidget(self.ch0_max_label,  1, 1)
        grid.addWidget(self.ch0_max_value,  1, 2)
        grid.addWidget(self.ch0_min_label,  1, 3)
        grid.addWidget(self.ch0_min_value,  1, 4)
        grid.addWidget(self.ch0_diff_label, 1, 5)
        grid.addWidget(self.ch0_diff_value, 1, 6)

        grid.addWidget(self.ch1_max_label,  2, 1)
        grid.addWidget(self.ch1_max_value,  2, 2)
        grid.addWidget(self.ch1_min_label,  2, 3)
        grid.addWidget(self.ch1_min_value,  2, 4)
        grid.addWidget(self.ch1_diff_label, 2, 5)
        grid.addWidget(self.ch1_diff_value, 2, 6)

        grid.addWidget(self.ch2_max_label,  3, 1)
        grid.addWidget(self.ch2_max_value,  3, 2)
        grid.addWidget(self.ch2_min_label,  3, 3)
        grid.addWidget(self.ch2_min_value,  3, 4)
        grid.addWidget(self.ch2_diff_label, 3, 5)
        grid.addWidget(self.ch2_diff_value, 3, 6)

        grid.addWidget(self.ch3_max_label,  4, 1)
        grid.addWidget(self.ch3_max_value,  4, 2)
        grid.addWidget(self.ch3_min_label,  4, 3)
        grid.addWidget(self.ch3_min_value,  4, 4)
        grid.addWidget(self.ch3_diff_label, 4, 5)
        grid.addWidget(self.ch3_diff_value, 4, 6)
        frame.setLayout(grid)

        return frame

    def signalSlot(self):
        self.startBtn.clicked.connect(self.configUdpFrame)
        self.stopBtn.clicked.connect(self.configUdpFrame)
        self.packetFrameDone.connect(self.udpCore.sendFrame)
        self.udpCore.recvDataReady[bytes, str, int].connect(self.processPendingDatagrams)
        pass

    @pyqtSlot()
    def configUdpFrame(self):
        sender = self.sender()

        head = 'AA555AA5 AA555AA5'
        cmd_num = 'aaddccaa'
        command = '00000005'
        data_len = '4'

        if sender.text() == '开始采集':
            data = '0000 0001'
        elif sender.text() == '停止采集':
            data = '0000 0000'

        self.udpTxPck.config(head=head, cmd_num=cmd_num, command=command, data_len=data_len, data=data)
        frame = self.udpTxPck.getFrame()
        self.packetFrameDone.emit(frame)

    @pyqtSlot(bytes, str, int)
    def processPendingDatagrams(self, datagram, host, port):
            data = b2a_hex(datagram)
            data = data.decode(encoding = 'utf-8')
            if data[24:32] != '80000006':
                self.waveQueue.put(data)

    @pyqtSlot(list)
    def updateChart(self, data):
        self.chart.update(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = CaptureBoard()
    ui.show()
    sys.exit(app.exec_())
