from PyQt5.QtWidgets import (QListWidgetItem, QListWidget)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (QObject, QThread, pyqtSignal, pyqtSlot)

import cv2 as cv

CV_SUPPORTED_FORMATS_FILTER = "CV-Supported Images (*.bmp *.dib *.jpeg *.jpg *.png *.webp *.pbm *.pgm *.ppm *.pxm *.pnm *.pfm *.sr *.ras *.tiff *.tif *.exr *.hdr *.pic)"

# Model for a stereo pair and whatever cool stuff we make with it
class StereoPair(QListWidgetItem):
    def __init__(self):
        super().__init__()
        self.rename("Unnamed Stereo Pair")
        self.left_image_cv = None
        self.right_image_cv = None
        self.left_image_preview = None
        self.right_image_preview = None
        self.disparity_map = None
        self.mesh = None

    def rename(self, text):
        if text != "":
            self.setText(text)

    def load_image(self, path, button):
        self.loading_thread = QThread()
        self.worker = ImageReadWorker(path)
        self.worker.moveToThread(self.loading_thread)
        self.loading_thread.started.connect(self.worker.load_image)
        self.worker.errored.connect(lambda: self.loadImageFailed(button))
        self.worker.finished.connect(lambda: self.loadImageFinished(path, button, self.worker.img))
        self.worker.finished.connect(self.loading_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.loading_thread.finished.connect(self.loading_thread.deleteLater)
        self.loading_thread.start()

    def loadImageFailed(self, button):
        button.clearImage()
        #ERRROR_DIALOG.showMessage("Failed to upload image")

    def loadImageFinished(self, path, button, img):
        if button.isLeft and img is not None:
            self.left_image_cv = img
            self.left_image_preview = QIcon(path)
            button.updateImage(self.left_image_preview)
        elif img is not None:
            self.right_image_cv = img
            self.right_image_preview = QIcon(path)
            button.updateImage(self.right_image_preview)

# Might want to extend this later, but QT manages Model/View interaction well with default list widget
class PairList(QListWidget):
    pass

class ImageReadWorker(QObject):
    finished = pyqtSignal()
    errored  = pyqtSignal()

    def __init__(self, path):
        super().__init__()
        self.path = path

    def load_image(self):
        print("loading image...")
        print(self.path)
        self.img = cv.imread(self.path)
        if self.img is None:
            print("CV imread failed")
            self.errored.emit()
        self.finished.emit()