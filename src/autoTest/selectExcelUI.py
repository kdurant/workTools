#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class SelectExcelUI(QWidget):
    def __init__(self, parent=None):
        super(SelectExcelUI, self).__init__(parent)


        group = self.groupBox()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(group)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)

    def groupBox(self):
        groupBox = QGroupBox('文件选择')

        self.loadFileBtn = QPushButton('选择文件')
        self.nameLabel= QLabel('file_name')


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.loadFileBtn)
        mainLayout.addWidget(self.nameLabel)

        groupBox.setLayout(mainLayout)
        return groupBox

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = SelectExcelUI()
    ui.show()
    sys.exit(app.exec_())
