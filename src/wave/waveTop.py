#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import binascii

from ..wave.laserConfig import *
from ..wave.selectFileUI import *
from ..wave.chart import Chart
from ..wave.oceanFormat import OceanFormat

ocean = OceanFormat()

class LaserDataAnaylze(QObject):
    updateCapNum = pyqtSignal(int)
    updateCapData = pyqtSignal(list)
    def __init__(self, file):
        super(LaserDataAnaylze, self).__init__()
        self.file = file

    def configPara(self, enableAnaylze=True, intervalTime=100):
        self.enableAnaylze = enableAnaylze
        self.intervalTime = intervalTime

    def analyze(self):
        curCapNum = -1
        capLaserData = ''
        with open(self.file, 'rb') as f:
            while True:
                if self.enableAnaylze == True:
                    text = f.read(4)
                    if not text:
                        break
                    text = binascii.b2a_hex(text).decode(encoding='utf8')
                    '''
                    1. 找到head后发送数据去分析
                    2. 清除列表内容
                    '''
                    if text == ocean.head:
                        ocean.setData(capLaserData, curCapNum)   #
                        if capLaserData:
                            l = []
                            Xdata, Ydata = ocean.getCh0Data()
                            l.append(Xdata)
                            l.append(Ydata)
                            Xdata, Ydata = ocean.getCh1Data()
                            l.append(Xdata)
                            l.append(Ydata)
                            Xdata, Ydata = ocean.getCh2Data()
                            l.append(Xdata)
                            l.append(Ydata)
                            Xdata, Ydata = ocean.getCh3Data()
                            l.append(Xdata)
                            l.append(Ydata)
                            self.updateCapData.emit(l)
                            QThread.msleep(self.intervalTime)
                        capLaserData = ''
                        capLaserData = ocean.head + capLaserData
                        curCapNum += 1
                        # if curCapNum % 100 == 0:      # 防止一直发送，阻塞主UI
                        self.updateCapNum.emit(curCapNum)
                    else:
                        capLaserData += text


class WaveTop(QWidget):
    configThreadSignal = pyqtSignal()

    def __init__(self):
        super(WaveTop, self).__init__()

        self.initUI()
        self.signalSlot()

    def initUI(self):
        self.selectFileUI = SelectFileUI()
        self.laserConfigUI = LaserConfigUI()
        self.laserChart = Chart()

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.selectFileUI)
        leftLayout.addWidget(self.laserConfigUI)
        leftLayout.addStretch(1)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.laserChart)

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
        self.analyze = LaserDataAnaylze(self.laserFile)
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
            self.configThreadSignal.emit()
        else:
            self.isLoadFile = False

    @pyqtSlot(int)
    def setCapNum(self, num):
        self.laserConfigUI.curWaveSerialLabel.setText(str(num))

    @pyqtSlot(list)
    def updateChart(self, data):
        self.laserChart.update(data)

    @pyqtSlot()
    def startAnaylzeThread(self):
        if self.laserFile:  # 如果加载了文件
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


