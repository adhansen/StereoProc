# import cv

from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTreeView)
from PyQt5.QtGui import (QPixmap)
from PyQt5.QtCore import (Qt, QAbstractItemModel, QModelIndex)

import typing

#fk all this, use QListWidget and QItemSelectionModel. Maybe keep the QAbstractItemModel for the actual data?

# class PairModel(QAbstractItemModel):
#     def __init__(self):
#         super().__init__()
#         self.stereo_pairs = [("a1", "a2"), ("b1", "b2")]

#     def rowCount(self, parent: QModelIndex = ...) -> int:
#         return len(self.stereo_pairs)

#     def columnCount(self, parent: QModelIndex = ...):
#         return 0

#     def data(self, index: QModelIndex, role: int = ...):
#         return self.stereo_pairs[QModelIndex.row()]

# class PairListWidget(QListWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.stereo_pairs = []
        

# class PairTreeView(QTreeView):
#     def __init__(self, parent):
#         super().__init__(parent)

class PairPreview(QWidget):
    def __init__(self, parent, label):
        super().__init__(parent)
        self.content = QVBoxLayout()
        self.content.setContentsMargins(30, 0, 0, 0)
        self.setLayout(self.content)

        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignCenter)
        self.preview = QLabel()
        self.updatePreview("img/placeholder.png")

        self.content.addWidget(self.preview)
        self.content.addWidget(self.label)
        self.content.insertStretch(-1, 1)

    def updatePreview(self, path):
        img = QPixmap(path).scaledToWidth(256)
        self.preview.setPixmap(img)