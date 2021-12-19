# import cv

from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTreeView)
from PyQt5.QtGui import (QPixmap)
from PyQt5.QtCore import (Qt, QAbstractListModel)

class PairModel(QAbstractListModel):
    def __init__(self):
        super()
        self.stereo_pairs = []

class PairTreeView(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)

class PairPreview(QWidget):
    def __init__(self, parent, label):
        super().__init__(parent)
        self.content = QVBoxLayout()
        self.content.setContentsMargins(30, 0, 0, 0)
        self.setLayout(self.content)

        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignCenter)
        self.preview = QLabel()
        self.updatePreview('img/placeholder.png')

        self.content.addWidget(self.preview)
        self.content.addWidget(self.label)
        self.content.insertStretch(-1, 1)

    def updatePreview(self, path):
        img = QPixmap(path).scaledToWidth(256)
        self.preview.setPixmap(img)