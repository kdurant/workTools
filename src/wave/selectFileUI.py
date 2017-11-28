#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class SelectFileUI(QWidget):
    def __init__(self, parent=None):
        super(SelectFileUI, self).__init__(parent)

        groupBox = QGroupBox('文件选择')

        self.loadFileBtn = QPushButton('选择文件')
        self.loadFileBtn.setIcon(QIcon('./images/open.svg'))
        self.loadFileBtn.setIconSize(QSize(48, 24))

        self.landRbtn = QRadioButton("&陆地")
        self.oceanRbtn = QRadioButton("&海洋")
        self.oceanRbtn.setChecked(True)

        hlyt = QHBoxLayout()
        hlyt.addWidget(self.loadFileBtn)
        hlyt.addWidget(self.landRbtn)
        hlyt.addWidget(self.oceanRbtn)
        groupBox.setLayout(hlyt)

        main_lyt = QHBoxLayout()
        main_lyt.addWidget(groupBox)
        main_lyt.addStretch(1)

        self.setLayout(main_lyt)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = SelectFileUI()
    ui.show()
    sys.exit(app.exec_())
