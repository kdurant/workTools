#-*- coding:utf-8 -*-
import binascii

from src.common.chart import Chart
from ..wave.laserConfig import *
from ..wave.laserFormat import LaserFormat
from ..wave.selectFileUI import *

laserWave = LaserFormat()

class LaserDataAnaylze(QObject):
    updateCapNum = pyqtSignal(int)
    updateCapData = pyqtSignal(list)
    def __init__(self):
        super(LaserDataAnaylze, self).__init__()
        self.runFlag = False

    def setFile(self, file, type = 'land'):
        self.file = file
        self.f = open(self.file, 'rb')
        self.fileType = type

    def configPara(self, runFlag=True, intervalTime=100):
        self.runFlag = runFlag
        self.intervalTime = intervalTime

    def analyze(self):
        print('hello')
        curCapNum = -1
        capLaserData = ''
        while True:
            if self.runFlag:
                text = self.f.read(4)
                if not text:
                    break
                text = binascii.b2a_hex(text).decode(encoding='utf8')
                '''
                1. 找到head后发送数据去分析
                2. 清除列表内容
                '''
                if text == laserWave.head and capLaserData:
                    laserWave.setData(capLaserData, curCapNum)   #
                    if capLaserData:
                        l = laserWave.getChData('oecan')
                        self.updateCapData.emit(l)
                        QThread.msleep(self.intervalTime)
                    capLaserData = ''
                    capLaserData = laserWave.head + capLaserData
                    curCapNum += 1
                    # if curCapNum % 100 == 0:      # 防止一直发送，阻塞主UI
                    self.updateCapNum.emit(curCapNum)
                else:
                    capLaserData += text
            else:
                capLaserData = ''


class WaveTop(QWidget):
    configThreadSignal = pyqtSignal()

    def __init__(self):
        super(WaveTop, self).__init__()

        self.initUI()
        self.signalSlot()
        self.configThread()

    def initUI(self):
        self.selectFileUI = SelectFileUI()
        self.laserConfigUI = LaserConfigUI()
        tab = QTabWidget()
        self.laserChart = Chart('apd', 'pmt1', 'pmt2', 'pmt3')
        tab.addTab(self.laserChart, 'laser')
        tab.addTab(QPushButton('motor'), 'motor cnt')

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.selectFileUI)
        leftLayout.addWidget(self.laserConfigUI)
        leftLayout.addStretch(1)

        rightLayout = QVBoxLayout()
        # rightLayout.addWidget(self.laserChart)
        rightLayout.addWidget(tab)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)
        mainLayout.setStretchFactor(leftLayout, 2)
        mainLayout.setStretchFactor(rightLayout, 5)
        self.setLayout(mainLayout)

    def signalSlot(self):
        self.selectFileUI.loadFileBtn.clicked.connect(self.getFile)
        self.laserConfigUI.startBtn.clicked.connect(self.startAnaylzeThread)
        self.laserConfigUI.pauseBtn.clicked.connect(self.pauseAnaylze)
        self.laserConfigUI.stopBtn.clicked.connect(self.pauseAnaylze)

        self.configThreadSignal.connect(self.configThread)

    @pyqtSlot()
    def configThread(self):
        self.analyze = LaserDataAnaylze()
        # self.analyze.configPara(True, self.laserFile, int(self.laserConfigUI.waveTimeEdit.text()))
        self.analyzeThread = QThread()
        self.analyze.moveToThread(self.analyzeThread)
        self.analyzeThread.started.connect(self.analyze.analyze)
        self.analyze.updateCapNum[int].connect(self.setCapNum)
        self.analyze.updateCapData[list].connect(self.updateChart)

    @pyqtSlot()
    def getFile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)

        if dlg.exec_():
            self.laserFile = dlg.selectedFiles()[0]
            self.isLoadFile = True
            # self.configThreadSignal.emit()
            if self.selectFileUI.landRbtn.isChecked():
                self.analyze.setFile(self.laserFile, 'land')
            else:
                self.analyze.setFile(self.laserFile, 'ocean')
        else:
            self.isLoadFile = False

    @pyqtSlot(int)
    def setCapNum(self, num):
        self.laserConfigUI.curWaveSerialLabel.setText(str(num))

    @pyqtSlot(list)
    def updateChart(self, data):
        self.laserChart.data = data
        self.laserChart.update()

    @pyqtSlot()
    def startAnaylzeThread(self):
        if self.laserFile:  # 如果加载了文件
            self.analyze.setFile(self.laserFile)
            self.analyze.configPara(True, int(self.laserConfigUI.waveTimeEdit.text()))
            self.laserConfigUI.startBtn.setEnabled(False)
            self.laserConfigUI.pauseBtn.setEnabled(True)
            self.laserConfigUI.stopBtn.setEnabled(True)
            if not self.analyzeThread.isRunning():
                self.analyzeThread.start()
        else:
            QMessageBox.information(self, "警告", "请先加载文件")

    @pyqtSlot()
    def pauseAnaylze(self):
        self.analyze.configPara(False)
        self.laserConfigUI.startBtn.setEnabled(True)
        self.laserConfigUI.pauseBtn.setEnabled(False)
        self.laserConfigUI.stopBtn.setEnabled(False)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = WaveTop()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())


