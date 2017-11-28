# -*- coding:utf-8 -*-

__version__ = 'v0.1.0'
__autor__ = 'kdurant'

import os
from binascii import a2b_hex, b2a_hex
from ..serial.serialUI import *
from ..serial.extendFunction import *

class SerialTop(SerialUI):
    dataReady = pyqtSignal(str, bool)
    def __init__(self):
        super(SerialTop, self).__init__()
        self.createToolBar()
        self.createStatusBar()

        self.autoTimer = QTimer()

        self.signalSlot()
        self.readConfigInfo()

    def signalSlot(self):
        self.serialInfo.serialDataReady[bytes].connect(self.anaylzeData)
        self.serialInfo.serialStateChanged[bool].connect(self.serialStatus)
        self.clearRecvBtn.clicked.connect(self.clearRecvData)
        self.saveRecvBtn.clicked.connect(self.saveRecvData)
        self.timeSendCb.clicked.connect(self.startAutoTimer)
        self.sendBtn.clicked.connect(self.getData)
        self.dataReady[str, bool].connect(self.serialInfo.sendData)
        self.autoTimer.timeout.connect(self.getData)
        self.loadFileBtn.clicked.connect(self.selectFile)
        self.sendFileBtn.clicked.connect(self.getFileData)
        self.hexSendRbtn.clicked.connect(self.editValidator)
        self.asciiSendRbtn.clicked.connect(self.editValidator)
        self.mutilString.dataReady[str, bool].connect(self.serialInfo.sendData)
        self.protocolFrame.dataReady[str, bool].connect(self.serialInfo.sendData)

    @pyqtSlot(bytes)
    def anaylzeData(self, recvData):
        self.recvCntBar.setText('接收字节：' + str(self.serialInfo.recvCnt))
        if self.hexRecvRbtn.isChecked():
            data = b2a_hex(recvData)
            data = data.decode('utf8')
        else:
            data = recvData
            data = data.decode('utf8')

        if not self.pauseReceiveCb.isChecked():
            if self.autoWrapCb.isChecked():
                self.recvText.insertPlainText(data + '\n')
            else:
                self.recvText.insertPlainText(data)

    @pyqtSlot()
    def getData(self):
        '''
        从发送文本框里获得需要发送的字符串
        :return:
        '''
        data = self.sendEdit.text()
        if len(data) == 0:
            QMessageBox.warning(self, '警告', '不能发送空内容')
            return
        if self.hexSendRbtn.isChecked():
            self.dataReady.emit(data , True)
        else:
            self.dataReady.emit(data, False)
        self.sendCntBar.setText('发送字节：' + str(self.serialInfo.sendCnt))

    @pyqtSlot()
    def clearRecvData(self):
        self.recvText.clear()
        self.serialInfo.recvCnt = 0
        self.serialInfo.sendCnt = 0
        self.sendCntBar.setText('发送字节：0')
        self.recvCntBar.setText('接收字节：0')

    @pyqtSlot()
    def saveRecvData(self):
        if self.recvText.toPlainText():
            filename = QFileDialog.getSaveFileName(self, 'save', 'serial.txt')
            try:
                with open(filename[0], 'w') as f:
                    f.write(self.recvText.toPlainText())
            except:
                pass
        else:
            QMessageBox.warning(self, '警告', '不能保存空白内容')

    @pyqtSlot()
    def startAutoTimer(self):
        if self.timeSendCb.isChecked():
            if not self.sendEdit.text():
                self.timeSendCb.setChecked(False)
                QMessageBox.warning(self, '警告', '没有可发送数据')
                return
            if self.openBtn.isEnabled():
                self.timeSendCb.setChecked(False)
                QMessageBox.warning(self, '警告', '没有打开串口')
                return
            self.autoTimer.start(int(self.timeEdit.text()))
        else:
            self.autoTimer.stop()

    @pyqtSlot()
    def selectFile(self):
        file = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          os.getcwd(),
                                                          "All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔

        self.loadFileEdit.setText(file[0])
        self.autoWrapCb.setChecked(False)

    @pyqtSlot()
    def getFileData(self):
        file = self.loadFileEdit.text()
        if len(file) == 0:
            return
        else:
            data = open(file, 'r', encoding='utf-8').read()
            if self.hexSendRbtn.isChecked():
                self.dataReady.emit(data, True)
            else:
                self.dataReady.emit(data, False)
            # data = data.decode('utf8')
            # self.dataReady.emit(data, False)
            self.sendCntBar.setText('发送字节：' + str(self.serialInfo.sendCnt))


    def showExtendUI(self):
        if self.extendUI.isHidden():
            self.extendUI.show()
        else:
            self.extendUI.hide()
        pass


    def createToolBar(self):
        # self.highAction = QAction(QIcon('images/high.svg'), "extend", self, triggered=self.showExtendUI)
        self.helpAction = QAction(QIcon('images/help.svg'), "help", self, triggered=self.showHelpWidget)
        self.aboutAction = QAction(QIcon('images/aboutTool.svg'), "about", self, triggered=self.aboutTool)
        toolbar = self.addToolBar('T')
        # new = QAction(QIcon("./images/new.png"), "new", self)
        #toolbar.addAction(self.highAction)
        toolbar.addAction(self.helpAction)
        toolbar.addAction(self.aboutAction)

    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.serialStatusBar = QLabel('串口状态：Close')
        self.recvCntBar = QLabel('接收字节：0')
        self.sendCntBar = QLabel('发送字节：0')
        self.bar3 = QLabel()
        self.statusBar.addWidget(self.serialStatusBar, 1)
        self.statusBar.addWidget(self.recvCntBar, 1)
        self.statusBar.addWidget(self.sendCntBar, 1)
        self.statusBar.addWidget(self.bar3, 1)
        self.setStatusBar(self.statusBar)

    def showHelpWidget(self):
        # self.helpWidget.show()
        if self.helpWidget.isHidden():
            self.helpWidget.show()
        else:
            self.helpWidget.hide()

    def closeEvent(self, event):
        self.saveConfigInfo()

    def readConfigInfo(self):
        try:
            data = open('config.txt', 'r')
            for line in data.readlines():
                line = line.replace('\n', '')
                select = line[22:23]
                content = line[36:]
                self.mutilString.selCbList[int(select)].setChecked(True)
                self.mutilString.hexEditList[int(select)].setText(content)
        except:
            pass
        pass

    def saveConfigInfo(self):
        data = open('config.txt', 'w')
        for i in range(0, len(self.mutilString.selCbList)):
            if self.mutilString.selCbList[i].isChecked():
                data.write('select line number is %s, content is %s\n' % (str(i), self.mutilString.hexEditList[i].text()))
        data.close()

    @pyqtSlot()
    def editValidator(self):
        if self.hexSendRbtn.isChecked():
            self.sendEdit.setValidator(QRegExpValidator(QRegExp("[a-fA-F0-9 ]+$")))
        else:
            self.sendEdit.setValidator(QRegExpValidator(QRegExp(".*")))

    @pyqtSlot(bool)
    def serialStatus(self, status):
        self.recvCntBar.setText('接收字节：' + str(self.serialInfo.recvCnt))
        self.sendCntBar.setText('发送字节：' + str(self.serialInfo.sendCnt))
        if status:
            self.serialStatusBar.setText('串口状态：Open')
        else:
            self.serialStatusBar.setText('串口状态：Close')

    @pyqtSlot()
    def aboutTool(self):
        QMessageBox.about(self, "介绍", "verison：" + __version__ + "\n" 
                                        "autor：" + __autor__ + "\n"
                                        'github: https://github.com/durant'
                                        )


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = SerialTop()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())
