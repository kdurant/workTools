#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from binascii import b2a_hex, a2b_hex

FILE_UNIT = 0x5000
class ReadDiskWidget(QWidget):
    fileInfoReady = pyqtSignal(list)
    def __init__(self):
        super(ReadDiskWidget, self).__init__()

        self.initUI()

        self.fileInfoReady[list].connect(self.addFileInfo)
        self.anaylzeBtn.clicked.connect(self.anaylzeFileName)
        self.saveBtn.clicked.connect(self.saveFile)

    def initUI(self):
        leftFrame = self.ctrlUI()
        rightFrame = self.fileInfoUI()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(leftFrame)
        mainLayout.addWidget(rightFrame)
        mainLayout.setStretchFactor(leftFrame, 1)
        mainLayout.setStretchFactor(rightFrame, 3)


        self.setLayout(mainLayout)
    def ctrlUI(self):
        self.diskReadComb = QComboBox()
        self.diskReadComb.addItems(self.diskInfo())
        self.anaylzeBtn = QPushButton('分析有效文件')
        self.saveBtn = QPushButton('保存')

        self.label = QLabel('文件读取进度：')
        self.progress = QProgressBar()
        self.progress.setMaximum(FILE_UNIT-1)
        self.progress.setMinimum(0)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.diskReadComb)
        mainLayout.addWidget(self.anaylzeBtn)
        mainLayout.addWidget(self.saveBtn)
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.progress)

        frame = QFrame()
        frame.setLayout(mainLayout)
        return frame

    def fileInfoUI(self):
        self.table = QTableWidget(0, 5)
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

    @staticmethod
    def diskInfo():
        info = ['\\\\.\\PHYSICALDRIVE2']
        # disk = open('\\\\.\\PHYSICALDRIVE0', 'rb')
        # try:
        #     disk = open('\\\\.\\PHYSICALDRIVE0', 'rb')
        # except PermissionError:
        #     info.append('\\\\.\\PHYSICALDRIVE0')
        # try:
        #     disk = open('\\\\.\\PHYSICALDRIVE1', 'rb')
        # except PermissionError:
        #     info.append('\\\\.\\PHYSICALDRIVE1')

        return info

    def readSector(self, drive, sector, data_len=512, mode='rb'):
        '''
        :param drive: 需要读取的硬盘
        :param sector: 需要读取的扇区编号
        :param data_len: 每次读取多少数据
        :param mode: 返回数据格式
        :return: 扇区数据
        '''
        drive.seek(sector * 512)
        data = drive.read(data_len)

        if mode == 'rb':
            return data
        elif mode == 'str':
            return data.hex()
        else:
            return

    def findFileName(self, disk, addr):
        '''
        :param disk:
        :param addr: 地址为unit地址，需要转换为sector地址 sector = unit * 32
        :return:
        '''
        data = self.readSector(disk, addr*32, data_len=128, mode='rb')
        if data.find(b'\xff') == -1:
            fileName = data.decode('utf8')
            data = self.readSector(disk, (addr+ 1)*32 , data_len=8, mode='rb')  # 读取文件起始地址，结束地址信息
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

    @pyqtSlot()
    def saveFile(self):
        items = self.table.selectedItems()

        fileName = items[0].text()
        fileStartUnit = items[0].text()
        fileEndUnit = items[0].text()

        file = open(fileName, 'w')
        disk = open(self.diskReadComb.setCurrentText(), 'rb')
        data = self.readSector(self, disk, fileStartUnit*16, data_len=512*32*(fileEndUnit-fileStartUnit), mode='rb')
        file.write(data)
        file.close()
        # for i in range(fileStartUnit, fileEndUnit):
        #     data = self.readSector(self, disk, i*16, data_len=512*32, mode='rb')
        #     file.write(data)

        # count = items.count()
        # print(count)