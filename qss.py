class test(object):
    pass
style = '''
QPushButton, QPushButton:focus, QPushButton:focus {
  background-color: %s;
  border: none;
  color: white;
  padding: 3px 20px;
}


QPushButton:hover, QPushButton:hover:focus {
  background-color: #2196f3;
  border-color: #ffffff;
}



QPushButton:pressed,
QPushButton:pressed:focus {
  background-color: #f50057;
  border: none;
  color: white;
}

QPushButton:disabled {
    color: #cccccc;
    background-color: #cccccc
    border: none
    
}
QComboBox
{
height: 20px;
border-radius: 4px;
border: 1px solid green;
/*background: green;*/
}
QComboBox:editable {
background: cyan;
}
QComboBox:!editable,QComboBox::drop-down:editable {
background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
stop:0#E1E1E1, stop: 0.4 #DDDDDD,
stop:0.5#D8D8D8, stop: 1.0 #D3D3D3);
}
QComboBox:!editable:on,QComboBox::drop-down:editable:on {
background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
stop:0#D3D3D3, stop: 0.4 #D8D8D8,
stop:0.5#DDDDDD, stop: 1.0 #E1E1E1);
}

QGroupBox
{
font-size: 12px;
background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0#E0E0E0, stop: 1 #FFFFFF);
border:2px solid gray;
border-radius:5px;
margin-top:10px;
}
QGroupBox::title {
subcontrol-origin: margin;
subcontrol-position: top center;/* position at the top center */
padding:03px;
background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0#FFEECE, stop: 1 #FFFFFF);
}


QTextEdit 
{
font-size: 12px;
background: rgb(153, 196, 149);
border-radius: 2px;
margin-top: 10px;
}

QLabel#bar0{
        color: rgb(128, 128, 192);
}

QToolTip {
    background-color: #000000;
    border: 2px solid #333333;
    color: yellow;
}

QLineEdit{
border:2px solid gray;
border-radius:5px;
padding:04px;
background: rgb(192, 192, 192);
selection-background-color: darkgray;
}

QLineEdit:read-only 
{
background: lightblue;
}

QCheckBox:enabled:checked{
        color: rgb(128, 128, 255);
}

QCheckBox::indicator {
width:18;
height:18;
}

QCheckBox::indicator:unchecked{
image: url(images/unchecked.svg);
}
QCheckBox::indicator:checked{
image: url(images/checked.svg);
}

QToolBar{
background: rgb(200, 200, 200);
spacing:3px;/* spacing between items in the tool bar */
}

QRadioButton:enabled:checked{
        color: rgb(128, 128, 255);
}

QRadioButton::indicator {
width:28;
height:28;
}

QRadioButton::indicator:unchecked{
image: url(images/rbtn_unchecked.png);
}
QRadioButton::indicator:checked{
image: url(images/rbtn_checked.png);
}

QTableView {
        border: 1px solid rgb(111, 156, 207);
        background: rgb(224, 238, 255);
        gridline-color: rgb(111, 156, 207);
}
QTableView::item {
        padding-left: 5px;
        padding-right: 5px;
        border: none;
        background: white;
        border-right: 1px solid rgb(111, 156, 207);
        border-bottom: 1px solid rgb(111, 156, 207);
}
QTableView::item:selected {
        background: #0080C0
}
QTableView::item:selected:!active {
        color: rgb(65, 65, 65);
}
QTableView::indicator {
        width: 20px;
        height: 20px;
}

QTabBar::tab {
    border: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    color: white;
    background: rgb(120, 170, 220);
    height: 28px;
    min-width: 85px;
    margin-right: 5px;
    padding-left: 5px;
    padding-right: 5px;
}
QTabBar::tab:hover {
    background: rgb(0, 78, 161);
}
QTabBar::tab:selected {
    color: white;
    background: rgb(0, 78, 161);
}

QStatusBar {
        background: rgb(187, 212, 238);
        border: 1px solid rgb(111, 156, 207);
        border-left: none;
        border-right: none;
        border-bottom: none;
}
QStatusBar::item {
    border: none;
    border-right: 1px solid rgb(111, 156, 207);
}

QProgressBar{
        border: none;
        color: white;
        text-align: center;
        background: rgb(68, 69, 73);
}
QProgressBar::chunk {
        border: none;
        background: rgb(0, 160, 230);
}
'''
