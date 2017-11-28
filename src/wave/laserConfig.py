#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class LaserConfigUI(QWidget):
    def __init__(self, parent=None):
        super(LaserConfigUI, self).__init__(parent)

        groupBox = QGroupBox('激光波形参数')
        # 参数
        self.waveIntervalEdit = QLineEdit('1')
        self.waveTimeEdit = QLineEdit('100')
        intValidator = QIntValidator(20, 1000)
        self.waveTimeEdit.setValidator(intValidator)
        self.curWaveSerialLabel = QLabel('0')
        formbox = QFormLayout()
        formbox.addRow('预览间隔', self.waveIntervalEdit)
        formbox.addRow('预览速度(ms):', self.waveTimeEdit)
        formbox.addRow('当前分析波形序号:', self.curWaveSerialLabel)


        # 控制按钮
        self.startBtn = QPushButton("开始")
        self.startBtn.setIconSize(QSize(48, 48))
        self.pauseBtn = QPushButton("暂停")
        self.pauseBtn.setEnabled(False)
        self.pauseBtn.setIconSize(QSize(48, 48))
        self.stopBtn = QPushButton("结束")
        self.stopBtn.setEnabled(False)
        self.stopBtn.setIconSize(QSize(48, 48))

        hbox = QHBoxLayout()
        hbox.addWidget(self.startBtn)
        hbox.addWidget(self.pauseBtn)
        hbox.addWidget(self.stopBtn)

        vbox = QVBoxLayout()
        vbox.addLayout(formbox)
        vbox.addLayout(hbox)
        groupBox.setLayout(vbox)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(groupBox)

        self.setLayout(mainLayout)
