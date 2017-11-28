#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ..wave.laserConfig import *
from ..wave.selectFileUI import *
from ..wave.chart import Chart
class WaveTop(QWidget):
    def __init__(self):
        super(WaveTop, self).__init__()

        self.initUI()

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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = WaveTop()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())


