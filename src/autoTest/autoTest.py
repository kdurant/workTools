from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
import sys
import xlrd
from binascii import a2b_hex, b2a_hex
# from .tcpServer import TcpServer
from tcpClient import TcpClient
from serialWidget import SerialWidget
from selectExcelUI import SelectExcelUI


class autoTest(QWidget):
    packetFrameDone = pyqtSignal([str])
    def __init__(self):
        super(autoTest, self).__init__()

        self.resize(QSize(1200, 600))
        self.initUI()
        self.signalSlot()
        self.expect_data = ''
        self.real_recv_data = ''

    def initUI(self):
        self.loadFileUI = SelectExcelUI()
        self.tcpClient = TcpClient()
        self.serialInfo = SerialWidget()

        self.startTestBtn = QPushButton("开始测试")
        hbox = QVBoxLayout()
        hbox.addWidget(self.loadFileUI)
        hbox.addWidget(self.tcpClient)
        hbox.addWidget(self.serialInfo)
        hbox.addWidget(self.startTestBtn)

        leftLayout = QVBoxLayout()
        leftLayout.addLayout(hbox)
        rightLayout = QVBoxLayout()

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        mainLayout.setStretchFactor(leftLayout, 1)
        mainLayout.setStretchFactor(rightLayout, 2)

        self.setLayout(mainLayout)


    def signalSlot(self):
        # self.loadFileBtn.clicked.connect(self.getFile)
        self.loadFileUI.loadFileBtn.clicked.connect(self.getFile)
        self.startTestBtn.clicked.connect(self.process)
        self.serialInfo.serialDataReady[bytes].connect(self.anaylzeUartData)
        pass

    def send_data(self, mode, data):

        QThread.msleep(1000)

        print('hello world')
        # print(self.real_recv_data)
        # if data.find('\n') == -1:
        #     print('use {0} send ------------{1}'.format(mode, data))
        # else:
        #     for line in data.split('\n'):
        #         print('use {0} send ~~~~~~~~~~~~~{1}'.format(mode, line))
        # pass

    @pyqtSlot()
    def process(self):
        start_line = 4
        start_col = 2
        for line in range(4, 100):
            line_context = self.table.row_values(line)
            if line_context[2] == '':
                pass
            else:
                self.send_data(line_context[2], line_context[3])

    @pyqtSlot()
    def getFile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)

        if dlg.exec_():
            self.selectedFile = dlg.selectedFiles()[0]
            self.loadFileUI.nameLabel.setText(self.selectedFile)
            self.isLoadFile = True
            wb = xlrd.open_workbook(filename=self.selectedFile)
            self.table = wb.sheets()[0]
        else:
            self.isLoadFile = False

    @pyqtSlot(bytes)
    def anaylzeUartData(self, recvData):
        self.real_recv_data += b2a_hex(recvData).decode('utf8')
        # print(self.real_recv_data)


    def queryStatus(self):
        if(self.tcpServer.linkRbtn.isChecked()):
            print(self.tcpServer.currentStatus())
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = autoTest()
    ui.show()
    sys.exit(app.exec_())
