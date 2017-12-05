#-*- coding:utf-8 -*-
#-*- coding:utf-8 -*-
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis, QScatterSeries
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src import *
import datetime

class Chart(QWidget):
    def __init__(self, ch0Name='ch0', ch1Name='ch1', ch2Name='ch2', ch3Name='ch3'):
        super(Chart, self).__init__()
        self.ch0Name = ch0Name
        self.ch1Name = ch1Name
        self.ch2Name = ch2Name
        self.ch3Name = ch3Name
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.chartUI())
        vbox.addWidget(self.controlUI())

        self.setLayout(vbox)

    def chartUI(self):
        self.chart1 = QLineSeries()
        self.chart1.setName(self.ch0Name)
        self.chart1.setPen(QPen(Qt.red))
        self.chart2 = QLineSeries()
        self.chart2.setName(self.ch1Name)
        self.chart2.setPen(QPen(Qt.darkYellow))
        self.chart3 = QLineSeries()
        self.chart3.setName(self.ch2Name)
        self.chart3.setPen(QPen(Qt.green))
        self.chart4 = QLineSeries()
        self.chart4.setName(self.ch3Name)
        self.chart4.setPen(QPen(Qt.blue))

        self.chart = QChart()
        self.chart.addSeries(self.chart1)
        self.chart.addSeries(self.chart2)
        self.chart.addSeries(self.chart3)
        self.chart.addSeries(self.chart4)
        self.chart.setAnimationOptions(QChart.AllAnimations)
        self.chart.setTitle("laser data")

        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.axis_x.setTickCount(10)
        self.axis_y.setTickCount(10)
        self.axis_x.setLabelFormat('%d')
        self.axis_y.setLabelFormat('%d')
        self.chart.setAxisX(self.axis_x, self.chart1)
        self.chart.setAxisY(self.axis_y, self.chart1)
        self.chart.setAxisX(self.axis_x, self.chart2)
        self.chart.setAxisY(self.axis_y, self.chart2)
        self.chart.setAxisX(self.axis_x, self.chart3)
        self.chart.setAxisY(self.axis_y, self.chart3)
        self.chart.setAxisX(self.axis_x, self.chart4)
        self.chart.setAxisY(self.axis_y, self.chart4)

        self.chartView = QChartView()
        self.chartView.setChart(self.chart)
        self.chartView.setRubberBand(QChartView.RectangleRubberBand)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        return self.chartView

    def controlUI(self):
        self.autoRefreshCb = QCheckBox('自动刷新')
        self.autoRefreshCb.setChecked(True)
        self.ch0Enable = QCheckBox(self.ch0Name)
        self.ch1Enable = QCheckBox(self.ch1Name)
        self.ch2Enable = QCheckBox(self.ch2Name)
        self.ch3Enable = QCheckBox(self.ch3Name)
        self.ch0Enable.setChecked(True)
        self.ch1Enable.setChecked(True)
        self.ch2Enable.setChecked(True)
        self.ch3Enable.setChecked(True)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.autoRefreshCb)
        hbox1.addWidget(self.ch0Enable)
        hbox1.addWidget(self.ch1Enable)
        hbox1.addWidget(self.ch2Enable)
        hbox1.addWidget(self.ch3Enable)

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

    def update(self, data):
        '''
        :param data:
        :return:
        '''
        # if len(data) == 2:
        #     x0Data, y0Data, x1Data, y1Data, x2Data, y2Data, x3Data, y3Data = data
        # elif len(data) == 4:
        #     x0Data, y0Data, x1Data, y1Data, x2Data, y2Data, x3Data, y3Data = data
        # elif len(data) == 6:
        #     x0Data, y0Data, x1Data, y1Data, x2Data, y2Data, x3Data, y3Data = data
        # elif len(data) == 8:
        x0Data, y0Data, x1Data, y1Data, x2Data, y2Data, x3Data, y3Data = data
        self.chart1.clear()
        self.chart2.clear()
        self.chart3.clear()
        self.chart4.clear()

        if self.autoRefreshCb.isChecked():
            self.axis_x.setRange(min(x0Data) - max(x0Data) // 10, max(x0Data) * 11 // 10)
            # self.axis_y.setRange(min(y0Data) - max(y0Data) // 10, max(y0Data) * 11 // 10)
            self.axis_y.setRange(0, 1000)
        try:
            for i in range(0, len(x0Data)):
                if self.ch0Enable.isChecked():
                    self.chart1.append(QPoint(x0Data[i], y0Data[i]))
                if self.ch1Enable.isChecked():
                    self.chart2.append(QPoint(x1Data[i], y1Data[i]))
                if self.ch2Enable.isChecked():
                    self.chart3.append(QPoint(x2Data[i], y2Data[i]))
                if self.ch3Enable.isChecked():
                    self.chart4.append(QPoint(x3Data[i], y3Data[i]))
        except:
            pass

        print(datetime.datetime.now())
        self.chartView.update()

    def fillAxisRange(self, data):
        x0Data, y0Data, x1Data, y1Data, x2Data, y2Data, x3Data, y3Data = data
        tmp = [min(x0Data), min(x1Data), min(x2Data), min(x3Data)]
        xDataMin = min(tmp)
        tmp = [max(x0Data), max(x1Data), max(x2Data), max(x3Data)]
        xDataMax = max(tmp)
        tmp = [min(y0Data), min(y1Data), min(y2Data), min(y3Data)]
        yDataMin = min(tmp)
        tmp = [max(y0Data), max(y1Data), max(y2Data), max(y3Data)]
        yDataMax = max(tmp)
        self.xDataMinLine.setText(str(xDataMin*9//10))
        self.xDataMaxLine.setText(str(xDataMax*11//10))
        self.yDataMinLine.setText(str(yDataMin*9//10))
        self.yDataMaxLine.setText(str(yDataMax*11//10))

    @pyqtSlot()
    # def setAxisRange(self, xDataMin, xDataMax, yDataMin, yDataMax):
    #     self.axis_x.setRange(xDataMin, xDataMax)
    #     self.axis_y.setRange(yDataMin, yDataMax)
    def setAxisRange(self):
        self.autoRefreshCb.setChecked(False)
        if self.xDataMinLine.text() and self.xDataMaxLine.text() and \
            self.yDataMinLine.text() and self.yDataMaxLine.text():
            self.axis_x.setRange(int(self.xDataMinLine.text()), int(self.xDataMaxLine.text()))
            self.axis_y.setRange(int(self.yDataMinLine.text()), int(self.yDataMaxLine.text()))
        else:
            QMessageBox.warning(self, '警告', '缺少参数')

    def mouseDoubleClickEvent(self, event):
        print('mouse double clicked')
        # self.chartView.resetTransform()
        # self.chart1.zoomReset()

    def mousePressEvent(self, event):
        print('mouse press')

    def mouseMoveEvent(self, event):
        print('mouse move')


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
        m = []
        x = []
        y = []
        z = []
        u = []
        for i in range(0, 50):
            m.append(i)
            x.append(random.randint(0, 100))
            y.append(random.randint(0, 100))
            z.append(random.randint(0, 100))
            u.append(random.randint(0, 100))

        self.chart.update([m, x, m, y, m, z, m, u])

if __name__ == "__main__":
    import sys
    import random
    import datetime

    app = QApplication([sys.argv])
    graph = TestUi()
    graph.show()

    sys.exit(app.exec_())
