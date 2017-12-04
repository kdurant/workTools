from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
import sys

from binascii import a2b_hex, b2a_hex
from src import *

import queue

class DataAnalyze(QObject):
    data_analyze_done = pyqtSignal()
    def __init__(self, queue, frame):
        super(DataAnalyze, self).__init__()
        self.q = queue
        self.frame = frame

    def work(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                self.frame.config(data)
                if self.frame.analyzeFrame() == True:
                    self.data_analyze_done.emit()


class CaptureBoard(QWidget):
    # data_analyze_start = pyqtSignal()
    send_udp_flag = pyqtSignal()
    def __init__(self):
        super(CaptureBoard, self).__init__()
        self.resize(QSize(1200, 600))

        self.cmd_cnt = 0
        self.frame = ''

        self.ad_sample_len = '160'
        self.udp_tx_pck = EncodeProtocol()
        self.udp_rx_pck = DecodeProtocol()
        self.udp_rx_queue = queue.Queue(-1)

        self.initUI()
        self.signalSlot()
        # self.threadConfig()

    def threadConfig(self):
        self.analyze = DataAnalyze(self.udp_rx_queue, self.udp_rx_pck)

        self.analyzeThread = QThread()
        # self.graphThread = QThread()

        self.analyze.moveToThread(self.analyzeThread)
        # self.graph.moveToThread(self.graphThread)

        self.analyzeThread.started.connect(self.analyze.work)
        # self.graphThread.started.connect(self.graph.work)

        # self.analyze.data_analyze_done.connect(self.graph.work)
        self.analyze.data_analyze_done.connect(self.updateChart)

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
        # self.send_udp_flag.connect(self.sendUdpFrame)
        pass

    @pyqtSlot()
    def configUdpFrame(self):
        self.cmd_cnt = int(self.cmd_num_edit.text())
        head = self.head_edit.text()
        cmd_num = self.cmd_num_edit.text()
        command = self.command_cb.currentText()
        data_len = self.data_len_edit.text()
        if self.command_cb.currentText() == 'AD采样长度':
            data = int(self.data_edit.text(), 10)
            data = data//8*8
            data = str(hex(data).replace('0x', ''))
            self.ad_sample_len = self.data_edit.text()
        else:
            data = self.data_edit.text()

        self.udp_tx_pck.config(head, cmd_num, command, data_len, data)
        self.frame = self.udp_tx_pck.getFrame()

        self.cmd_cnt += 1
        self.cmd_num_edit.setText(str(self.cmd_cnt))

        self.frame = a2b_hex(self.frame)
        self.send_udp_flag.emit()

    @pyqtSlot()
    def processPendingDatagrams(self):
        while self.udpSocket.hasPendingDatagrams():
            # print(self.udpRecSocket.pendingDatagramSize())
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            datagram = b2a_hex(datagram)
            datagram = datagram.decode(encoding = 'utf-8')
            # print(datagram)
            if self.bind_btn.text() == '已经连接':
                self.udp_rx_queue.put(datagram)
                self.rec_data_text.append(datagram)


    def updateChart(self):
        self.ch0_data.clear()
        self.ch1_data.clear()
        self.ch2_data.clear()
        self.ch3_data.clear()
        for i in self.udp_rx_pck.ch0_data_x:
            self.ch0_data.append(QPointF(i, self.udp_rx_pck.ch0_ydata[i]))
            self.ch1_data.append(QPointF(i, self.udp_rx_pck.ch1_ydata[i]))
            self.ch2_data.append(QPointF(i, self.udp_rx_pck.ch2_ydata[i]))
            self.ch3_data.append(QPointF(i, self.udp_rx_pck.ch3_ydata[i]))
        self.chartView.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = CaptureBoard()
    ui.show()
    sys.exit(app.exec_())
