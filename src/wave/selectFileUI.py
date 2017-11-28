#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class SelectFileUI(QWidget):
    def __init__(self, parent=None):
        super(SelectFileUI, self).__init__(parent)


        group = self.groupBox()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(group)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

    def groupBox(self):
        groupBox = QGroupBox('文件选择')

        self.loadFileBtn = QPushButton('选择文件')

        self.landRbtn = QRadioButton("&陆地")
        self.oceanRbtn = QRadioButton("&海洋")
        self.oceanRbtn.setChecked(True)

        hbox = QHBoxLayout()
        hbox.addWidget(self.landRbtn)
        hbox.addWidget(self.oceanRbtn)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.loadFileBtn)
        mainLayout.addLayout(hbox)

        groupBox.setLayout(mainLayout)
        return groupBox

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = SelectFileUI()
    ui.show()
    sys.exit(app.exec_())
