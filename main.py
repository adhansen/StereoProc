#!/usr/bin/python

from PyQt6.QtWidgets import  QApplication
from mainwindow import MainWindow

import sys

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()