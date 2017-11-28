#-*- coding:utf-8 -*-
#-*- coding:utf-8 -*-
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Chart(QWidget):
    def __init__(self):
        super(Chart, self).__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.chartUI())
        vbox.addWidget(self.controlUI())

        self.setLayout(vbox)

    def chartUI(self):
        self.chart1 = QLineSeries()
        self.chart1.setName('chart1')

        pen = QPen()
        # pen.setWidthF(.2)
        pen.setColor(Qt.red)
        self.chart1.setPen(pen)

        self.chart = QChart()
        # self.chart.legend().hide()
        self.chart.addSeries(self.chart1)
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.chart.setTitle("basic class")

        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.chart.setAxisX(self.axis_x, self.chart1)
        self.chart.setAxisY(self.axis_y, self.chart1)

        self.chartView = QChartView()
        self.chartView.setChart(self.chart)
        self.chartView.setRubberBand(QChartView.RectangleRubberBand)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        return self.chartView

    def controlUI(self):
        self.ch0Enable = QCheckBox('Ch0 Enable')
        self.ch0Enable.setChecked(True)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.ch0Enable)
        hbox1.addStretch(1)

        self.xDataMinLabel = QLabel('x min:')
        self.xDataMaxLabel = QLabel('x max:')
        self.yDataMinLabel = QLabel('y min:')
        self.yDataMaxLabel = QLabel('y max:')

        self.xDataMinLine = QLineEdit()
        self.xDataMaxLine = QLineEdit()
        self.yDataMinLine = QLineEdit()
        self.yDataMaxLine = QLineEdit()
        self.setBtn = QPushButton('设置')

        hbox = QHBoxLayout()
        hbox.addWidget(self.xDataMinLabel)
        hbox.addWidget(self.xDataMinLine)
        hbox.addWidget(self.xDataMaxLabel)
        hbox.addWidget(self.xDataMaxLine)
        hbox.addWidget(self.yDataMinLabel)
        hbox.addWidget(self.yDataMinLine)
        hbox.addWidget(self.yDataMaxLabel)
        hbox.addWidget(self.yDataMaxLine)
        hbox.addWidget(self.setBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox1)
        mainLayout.addLayout(hbox)
        frame = QFrame()
        frame.setLayout(mainLayout)

        self.setBtn.clicked.connect(self.setAxisRange)
        return frame

    def update(self, xData, yData):
        '''
        :param xData: list, store x coordinate data
        :param yData: list, store y coordinate data
        :return:
        '''

        self.chart1.clear()
        self.axis_x.setRange(min(xData)- max(xData)//10, max(xData)*11//10)
        self.axis_y.setRange(min(yData)- max(yData)//10, max(yData)*11//10)
        print(datetime.datetime.now())
        for i in range(0, len(xData)):
            if self.ch0Enable.isChecked():
                # self.chart1.append(QPoint(xData[i], yData[i]))
                self.chart1.append(xData[i], yData[i])
        print(datetime.datetime.now())

        self.chart1.clear()
        print(datetime.datetime.now())
        for i in range(0, len(xData)):
            if self.ch0Enable.isChecked():
                self.chart1.append(QPoint(xData[i], yData[i]))
        print(datetime.datetime.now())
        self.chartView.update()

    @pyqtSlot()
    # def setAxisRange(self, xDataMin, xDataMax, yDataMin, yDataMax):
    #     self.axis_x.setRange(xDataMin, xDataMax)
    #     self.axis_y.setRange(yDataMin, yDataMax)
    def setAxisRange(self):
        self.axis_x.setRange(int(self.xDataMinLine.text()), int(self.xDataMaxLine.text()))
        self.axis_y.setRange(int(self.yDataMinLine.text()), int(self.yDataMaxLine.text()))


class TestUi(QWidget):
    def __init__(self):
        super(TestUi, self).__init__()

        self.chart = Chart()
        self.btn = QPushButton('push')

        self.btn.clicked.connect(self.generateData)

        vbox = QVBoxLayout()
        vbox.addWidget(self.chart)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

    def generateData(self):
        x = []
        y = []
        for i in range(0, 1000):
            x.append(i)
            y.append(random.randint(0, 100))

        self.chart.update(x, y)

if __name__ == "__main__":
    import sys
    import random
    import datetime

    app = QApplication([sys.argv])
    graph = TestUi()
    graph.show()

    sys.exit(app.exec_())