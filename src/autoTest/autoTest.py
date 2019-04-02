from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
import sys
import xlrd

class SelectExcelUI(QWidget):
    def __init__(self, parent=None):
        super(SelectExcelUI, self).__init__(parent)

        self.sendMode = ''
        self.recvMode = ''
        self.sendData = ''
        self.recvData = ''

        group = self.groupBox()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(group)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

    def groupBox(self):
        groupBox = QGroupBox('文件选择')

        self.loadFileBtn = QPushButton('选择文件')
        self.nameLabel= QLabel('file_name')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.loadFileBtn)
        mainLayout.addWidget(self.nameLabel)

        groupBox.setLayout(mainLayout)
        return groupBox


######################################################################
class autoTest(QWidget):
    packetFrameDone = pyqtSignal([str])
    def __init__(self):
        super(autoTest, self).__init__()
        self.resize(QSize(1200, 600))
        self.initUI()
        self.signalSlot()

    def initUI(self):
        self.loadFileUI = SelectExcelUI()

        self.startTestBtn = QPushButton("开始测试")
        hbox = QVBoxLayout()
        hbox.addWidget(self.loadFileUI)
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
        pass

    @pyqtSlot()
    def process(self):
        start_line = 4
        start_col = 2
        for line in range(4, 90):
            line_context = self.table.row(line)
            if line_context[2] == 'empty:\'\'':
                print('----------------')
            else:
                print(line_context[2])


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = autoTest()
    ui.show()
    sys.exit(app.exec_())
