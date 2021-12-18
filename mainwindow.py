from PyQt6.QtWidgets import (QMainWindow)
from PyQt6.QtGui import (QIcon)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("StereoProc")
        self.setWindowIcon(QIcon("img/favicon.png"))
        self.setFixedSize(900, 480)