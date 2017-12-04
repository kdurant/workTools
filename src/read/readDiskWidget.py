#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from binascii import b2a_hex, a2b_hex
from ..common.misc import *
import datetime

FILE_UNIT = 0x5000


class WriteData(QObject):
    fileWriteDone = pyqtSignal()
    def __init__(self):
        super(WriteData, self).__init__()
        self.currentAddr = 0

    def config(self, diskName, item):
        self.diskName = diskName
        self.items = item
        pass

    def saveFile(self):
        fileName = self.items[0].text()
        fileStartUnit = int(self.items[1].text(), 16)
        fileEndUnit = int(self.items[2].text(), 16)

        file = open(fileName + '.bin', 'wb')
        disk = open(self.diskName, 'rb')
        n = datetime.datetime.now()
        for addr in range(fileStartUnit, fileEndUnit):
            self.currentAddr = addr
            data = readSector(disk, addr*32, data_len=32*512, mode='rb')
            file.write(data)
        m = datetime.datetime.now()
        self.writeFileTime = m-n
        file.close()
        disk.close()
        self.fileWriteDone.emit()

class ReadDiskWidget(QWidget):
    fileInfoReady = pyqtSignal(list)
    startWriteFile = pyqtSignal()

    def __init__(self):
        super(ReadDiskWidget, self).__init__()

        self.initUI()

        self.timer = QTimer()
        self.timer.start(100)

        self.timer.timeout.connect(self.setProgress)

        self.fileInfoReady[list].connect(self.addFileInfo)
        self.anaylzeBtn.clicked.connect(self.anaylzeFileName)
        self.saveBtn.clicked.connect(self.saveFile)

        self.writeThread = QThread()
        self.writeFile = WriteData()

        self.writeFile.moveToThread(self.writeThread)
        self.writeThread.start()

        self.startWriteFile.connect(self.writeFile.saveFile)
        self.writeFile.fileWriteDone.connect(self.fileHint)

    def initUI(self):
        leftFrame = self.ctrlUI()
        rightFrame = self.fileInfoUI()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(leftFrame)
        mainLayout.addWidget(rightFrame)
        mainLayout.setStretchFactor(leftFrame, 2)
        mainLayout.setStretchFactor(rightFrame, 5)


        self.setLayout(mainLayout)
    def ctrlUI(self):
        self.diskReadComb = QComboBox()
        self.diskReadComb.addItems(diskInfo())
        self.anaylzeBtn = QPushButton('分析有效文件')
        self.saveBtn = QPushButton('保存')

        self.label = QLabel('文件写入进度：')
        self.progress = QProgressBar()
        self.progress.setMaximum(FILE_UNIT-1)
        self.progress.setMinimum(0)

        timeLabel = QLabel('时间：')
        self.timeLine = QLineEdit()
        self.timeLine.setReadOnly(True)

        hbox = QHBoxLayout()
        hbox.addWidget(timeLabel)
        hbox.addWidget(self.timeLine)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.diskReadComb)
        mainLayout.addWidget(self.anaylzeBtn)
        mainLayout.addStretch(1)
        mainLayout.addWidget(self.saveBtn)
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.progress)
        mainLayout.addLayout(hbox)

        frame = QFrame()
        frame.setLayout(mainLayout)
        return frame

    def fileInfoUI(self):
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['文件名', '起始unit', '结束unit', '文件大小'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        vbox = QVBoxLayout()
        vbox.addWidget(self.table)

        frame = QFrame()
        frame.setLayout(vbox)

        return frame

    def anaylzeFileName(self):
        try:
            file = self.diskReadComb.currentText()
            disk = open(file, 'rb')
        except:
            print('error')
        for unitAddr in range(0, FILE_UNIT-1):
            if unitAddr % 2 == 0:
                info = self.findFileName(disk, unitAddr)
                if info == False:
                    return
                else:
                    self.fileInfoReady.emit(info)

    def findFileName(self, disk, addr):
        '''
        :param disk:
        :param addr: 地址为unit地址，需要转换为sector地址 sector = unit * 32
        :return:
        '''
        data = readSector(disk, addr*32, data_len=128, mode='rb')
        if data.find(b'\xff') == -1:
            fileName = data.decode('utf8')
            fileName = fileName.replace('\0', '')
            data = readSector(disk, (addr+ 1)*32 , data_len=8, mode='rb')  # 读取文件起始地址，结束地址信息
            fileStartAddr = b2a_hex(data[:4]).decode()
            fileEndAddr = b2a_hex(data[4:8]).decode()
            fileInfo = [fileName, fileStartAddr, fileEndAddr]
            return fileInfo
        else:
            return False

    @pyqtSlot(list)
    def addFileInfo(self, info):
        rowIndex = self.table.rowCount()
        self.table.setRowCount(rowIndex+1)

        for i in range(0, 3):
            item = QTableWidgetItem()
            item.setText(info[i])
            self.table.setItem(rowIndex, i, item)

        fileSize = (int(info[2], 16)-int(info[1], 16))*16/(1024*1024)
        item = QTableWidgetItem()
        item.setText(str(fileSize)[:5])
        self.table.setItem(rowIndex, 3, item)

        self.table.resizeColumnsToContents()

    @pyqtSlot()
    def saveFile(self):
        items = self.table.selectedItems()
        if items:
            self.progress.setMinimum(int(items[1].text(), 16))
            self.progress.setMaximum(int(items[2].text(), 16)-1)
            self.writeFile.config(self.diskReadComb.currentText(), items)
            self.startWriteFile.emit()
        else:
            QMessageBox.warning(self, '警告', '请选择需要写入的文件')

    @pyqtSlot()
    def fileHint(self):
        self.timeLine.setText(str(self.writeFile.writeFileTime))
        QMessageBox.information(self, '信息', '文件写入成功')

    @pyqtSlot()
    def setProgress(self):
        self.progress.setValue(self.writeFile.currentAddr)