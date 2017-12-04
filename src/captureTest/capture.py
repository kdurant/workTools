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


class CaptureBoard(QMainWindow):
    # data_analyze_start = pyqtSignal()
    send_udp_flag = pyqtSignal()
    def __init__(self):
        super(CaptureBoard, self).__init__()
        self.setWindowTitle('协议调试工具')
        self.setWindowIcon(QIcon('images/network.svg'))
        self.resize(QSize(1200, 600))

        self.cmd_cnt = 0
        self.frame = ''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

        pe = QPalette()
        self.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, QColor(185, 185, 185))
        self.setPalette(pe)

        self.ad_sample_len = '160'
        self.udp_tx_pck = EncodeProtocol()
        self.udp_rx_pck = DecodeProtocol()
        self.udp_rx_queue = queue.Queue(-1)

        self.initUI()
        self.udpConfig()
        self.signalSlot()
        self.threadConfig()

    def udpConfig(self):
        self.udpSocket = QUdpSocket(self)
        self.udpSocket.bind(int(self.master_port.text()))
        self.udpSocket.readyRead.connect(self.processPendingDatagrams)

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
        self.set_command = self.udpCommandUI()
        self.info = self.sysParameterUI()
        self.rec_data = self.receiveDataUI()
        self.ad_chart = self.previewDataUI()


        left_hbox = QVBoxLayout()
        left_hbox.addWidget(self.info)
        # left_hbox.addStretch(1)

        left_hbox.addWidget(self.set_command)
        left_hbox.addWidget(self.rec_data)

        right_hbox = QVBoxLayout()
        right_hbox.addWidget(self.ad_chart)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_hbox)
        main_layout.addLayout(right_hbox)
        main_layout.setStretchFactor(left_hbox, 1)
        main_layout.setStretchFactor(right_hbox, 2)

        self.main_frame = QWidget(self)
        self.main_frame.setLayout(main_layout)
        self.setCentralWidget(self.main_frame)

    def sysParameterUI(self):
        groupBox = QGroupBox('参数设置')
        self.master_ip = QLineEdit('192.168.1.166')
        # self.master_ip.setFixedWidth(120)
        self.master_port = QLineEdit('6666')
        # self.master_port.setFixedWidth(120)

        self.target_ip = QLineEdit('192.168.1.101')
        # self.target_ip.setFixedWidth(120)
        self.target_port = QLineEdit('5555')
        # self.target_port.setFixedWidth(120)

        self.bind_label = QLabel()
        self.bind_label.setPixmap(QPixmap('images/inactive.svg').scaled(QSize(24, 24)))
        self.bind_btn = QPushButton('已经断开')
        # self.bind_btn.setIcon(QIcon('images/bind.svg'))
        # self.bind_btn.setIconSize(QSize(256, 32))

        label = QLabel()
        label.setPixmap(QPixmap('images/debug.svg').scaled(QSize(150, 150)))

        form = QFormLayout()
        form.addRow('本机IP地址：', self.master_ip)
        form.addRow('本机端口号：', self.master_port)
        form.addRow('设备IP地址：', self.target_ip)
        form.addRow('UDP端口号：', self.target_port)
        form.addRow(self.bind_btn, self.bind_label)

        hbox = QHBoxLayout()
        hbox.addLayout(form)
        hbox.addStretch(1)
        hbox.addWidget(label)
        hbox.addStretch(1)

        groupBox.setLayout(hbox)
        return groupBox

    def udpCommandUI(self):
        groupBox = QGroupBox('发送命令设置')

        self.head_label = QLabel('帧头                ')
        self.cmd_num_label = QLabel('指令序号')
        self.command_label = QLabel('指令')
        self.pck_num_label = QLabel('包序号')
        self.data_len_label = QLabel('数据长度')
        self.data_label = QLabel('数据                       ')
        self.check_sum_label = QLabel('校验和       ')

        self.head_edit = QLineEdit('AA555AA5 AA555AA5')
        # self.head_edit.setReadOnly(True)
        self.cmd_num_edit = QLineEdit('0')
        # self.cmd_num_edit.setReadOnly(True)
        self.command_cb = QComboBox()
        self.command_cb.addItem('系统复位')
        self.command_cb.addItem('读取设备参数')
        self.command_cb.addItems(['透传激光参数', '激光重频', '激光器开关'])
        self.command_cb.addItems(['AD起始位置', 'AD采样长度', 'AD采集状态'])

        self.pck_num_edit = QLineEdit('0')
        self.pck_num_edit.setReadOnly(True)
        self.data_len_edit = QLineEdit('4')
        self.data_edit = QLineEdit('00 00 00 01')
        # self.data_edit.setPlaceholderText('00 00 00 01')
        self.check_sum_edit = QLineEdit('04 03 02 01')
        self.check_sum_edit.setReadOnly(True)

        self.send_btn = QPushButton()
        self.send_btn.setIcon(QIcon('images/send.svg'))
        self.send_btn.setIconSize(QSize(64, 32))

        grid = QGridLayout()
        # layout.setSpacing(10)
        # layout.addWidget(self.head_label, 1, 1)
        # layout.addWidget(self.cmd_num_label, 1, 2)
        grid.addWidget(self.command_label, 1, 3)
        # layout.addWidget(self.pck_num_label, 1, 4)
        # layout.addWidget(self.data_len_label, 1, 5)
        grid.addWidget(self.data_label, 1, 6)
        # layout.addWidget(self.check_sum_label, 1, 7)

        # layout.addWidget(self.head_edit, 2, 1)
        # layout.addWidget(self.cmd_num_edit, 2, 2)
        grid.addWidget(self.command_cb, 2, 3)
        # layout.addWidget(self.pck_num_edit, 2, 4)
        # layout.addWidget(self.data_len_edit, 2, 5)
        grid.addWidget(self.data_edit, 2, 6)
        # layout.addWidget(self.check_sum_edit, 2, 7)

        hbox = QHBoxLayout()
        hbox.addLayout(grid)
        hbox.addWidget(self.send_btn)

        groupBox.setLayout(hbox)
        return groupBox

    def receiveDataUI(self):
        group = QGroupBox('接受数据')
        self.rec_data_text = QTextEdit()
        self.clear_btn = QPushButton()
        self.clear_btn.setIcon(QIcon('images/clear.svg'))

        layout = QVBoxLayout()
        layout.addWidget(self.rec_data_text)
        layout.addWidget(self.clear_btn)
        group.setLayout(layout)
        return group

    def previewDataUI(self):
        frame = QFrame()
        self.ch0_max_label = QLabel('ch0 max value:')
        self.ch1_max_label = QLabel('ch1 max value:')
        self.ch2_max_label = QLabel('ch2 max value:')
        self.ch3_max_label = QLabel('ch3 max value:')
        self.ch0_max_value = QLineEdit()
        self.ch1_max_value = QLineEdit()
        self.ch2_max_value = QLineEdit()
        self.ch3_max_value = QLineEdit()
        self.ch0_min_label = QLabel('ch0 min value:')
        self.ch1_min_label = QLabel('ch1 min value:')
        self.ch2_min_label = QLabel('ch2 min value:')
        self.ch3_min_label = QLabel('ch3 min value:')
        self.ch0_min_value = QLineEdit()
        self.ch1_min_value = QLineEdit()
        self.ch2_min_value = QLineEdit()
        self.ch3_min_value = QLineEdit()
        self.ch0_diff_label = QLabel('ch0 f-f value:')
        self.ch1_diff_label = QLabel('ch1 f-f value:')
        self.ch2_diff_label = QLabel('ch2 f-f value:')
        self.ch3_diff_label = QLabel('ch3 f-f value:')
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

        self.chart = self.adChartUI()

        hbox = QHBoxLayout()


        self.ch0_show_enable = QCheckBox('show ch0')
        self.ch1_show_enable = QCheckBox('show ch1')
        self.ch2_show_enable = QCheckBox('show ch2')
        self.ch3_show_enable = QCheckBox('show ch3')
        self.ch0_show_enable.setChecked(True)
        self.ch1_show_enable.setChecked(True)
        self.ch2_show_enable.setChecked(True)
        self.ch3_show_enable.setChecked(True)
        hbox.addWidget(self.ch0_show_enable)
        hbox.addWidget(self.ch1_show_enable)
        hbox.addWidget(self.ch2_show_enable)
        hbox.addWidget(self.ch3_show_enable)
        vbox = QVBoxLayout()

        # vbox.addLayout(grid)
        vbox.addWidget(self.chart)
        vbox.addLayout(hbox)
        frame.setLayout(vbox)

        return frame
    def signalSlot(self):
        self.bind_btn.clicked.connect(self.udpLinkStatus)
        self.send_btn.clicked.connect(self.configUdpFrame)
        self.clear_btn.clicked.connect(self.rec_data_text.clear)
        self.command_cb.currentIndexChanged.connect(self.adaptCommandParameter)
        self.send_udp_flag.connect(self.sendUdpFrame)

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
    def sendUdpFrame(self):
        self.udpSocket.writeDatagram(QByteArray(self.frame), QHostAddress(self.target_ip.text()),
                                     int(self.target_port.text()))

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

    @pyqtSlot()
    def adaptCommandParameter(self):
        if self.command_cb.currentText() == '系统复位':
            self.data_edit.setText('00 00 00 01')
        elif self.command_cb.currentText() == '读取设备参数':
            self.data_edit.setText('00 00 00 01')
        elif self.command_cb.currentText() == '激光重频':
            self.data_edit.setText('100')
        elif self.command_cb.currentText() == 'AD起始位置':
            self.data_edit.setText('0')
        elif self.command_cb.currentText() == 'AD采样长度':
            self.data_edit.setText(self.ad_sample_len)

        elif self.command_cb.currentText() == 'AD采集状态':
            self.data_edit.setText('f')
        else:
            pass

        if self.command_cb.currentText() == 'AD采样长度':
            self.data_label.setText('数据(DEC)')
        else:
            self.data_label.setText('数据(HEX)')

    @pyqtSlot()
    def udpLinkStatus(self):
        if self.bind_btn.text() == '已经断开':
            self.bind_btn.setText('已经连接')
            self.bind_label.setPixmap(QPixmap('images/active.svg').scaled(QSize(24, 24)))
        else:
            self.bind_btn.setText('已经断开')
            self.bind_label.setPixmap(QPixmap('images/inactive.svg').scaled(QSize(24, 24)))

        if not self.analyzeThread.isRunning():
            self.analyzeThread.start()

        #if not self.graphThread.isRunning():
            #self.graphThread.start()

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
