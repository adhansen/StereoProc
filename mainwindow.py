from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QMainWindow)
from PyQt5.QtGui import (QIcon)

from pairmodelview import (PairModel, PairTreeView, PairPreview)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StereoProc")
        self.setWindowIcon(QIcon("img/favicon.png"))
        self.setFixedSize(900, 480)

        self.setCentralWidget(QWidget(self))
        self.content = QHBoxLayout()
        self.content.setContentsMargins(10, 10, 10, 10)
        self.centralWidget().setLayout(self.content)

        self.pair_model = PairModel()
        self.pair_tree_view = PairTreeView(self)
        self.pair_preview_left = PairPreview(self, "Left")
        self.pair_preview_right = PairPreview(self, "Right")

        self.content.addWidget(self.pair_tree_view)
        self.content.addWidget(self.pair_preview_left)
        self.content.addWidget(self.pair_preview_right)
