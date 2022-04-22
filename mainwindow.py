from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow, QPushButton,
                             QLineEdit, QSpacerItem, QSizePolicy, QFileDialog)
from PyQt5.QtGui import (QIcon, QPixmap)
from PyQt5.QtCore import (pyqtSlot, pyqtSignal, QSize)

from stereomodel import * #FIXME don't import the worker shit
from matplotlib import pyplot as plt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StereoProc")
        self.setWindowIcon(QIcon("img/favicon.png"))
        self.setFixedSize(900, 480)

        # Outermost layout
        self.setCentralWidget(QWidget(self))
        self.content = QHBoxLayout()
        self.centralWidget().setLayout(self.content)

        # Inner layours
        self.left_column = QWidget()
        self.left_column.setMaximumWidth(250)
        self.left_column_layout = QVBoxLayout()
        self.left_column.setLayout(self.left_column_layout)

        # Left column user widgets
        self.pair_list_label = QLabel(self)
        self.pair_list = PairList()
        self.list_button_layout = QHBoxLayout()
        self.renaming_layout = QHBoxLayout()
        self.renaming_input = QLineEdit(self)
        self.renaming_button = QPushButton(self)
        self.add_pair_button = QPushButton(self)
        self.delete_pair_button = QPushButton(self)

        self.list_button_layout.addWidget(self.add_pair_button)
        self.list_button_layout.addWidget(self.delete_pair_button)
        self.renaming_layout.addWidget(self.renaming_input)
        self.renaming_layout.addWidget(self.renaming_button)
        self.left_column_layout.addWidget(self.pair_list_label)
        self.left_column_layout.addWidget(self.pair_list)
        self.left_column_layout.addLayout(self.renaming_layout)
        self.left_column_layout.addLayout(self.list_button_layout)

        self.pane = SelectionPane(self)
        self.content.addWidget(self.left_column)
        self.content.addWidget(self.pane)

        # Init UI Text
        self.pair_list_label.setText("Stereo pairs:")
        self.renaming_button.setText("Rename")
        self.add_pair_button.setText("Add")
        self.delete_pair_button.setText("Delete")

        # Signals
        self.pair_list.currentRowChanged.connect(self.listItemChangeEvent)
        self.add_pair_button.clicked.connect(lambda: self.pair_list.addItem(StereoPair()))
        self.delete_pair_button.clicked.connect(self.listDeleteEvent)
        self.renaming_button.clicked.connect(self.listRenameEvent)
        self.renaming_input.returnPressed.connect(self.listRenameEvent)

    # Main window slots
    @pyqtSlot()
    def listItemChangeEvent(self):
        selected_item = self.pair_list.currentItem()
        # Last item is deleted
        if selected_item is None:
            self.pane.hide()
            return
        # Otherwise update previews and so forth
        self.pane.left_upload.updateImage(selected_item.left_image_preview)
        self.pane.right_upload.updateImage(selected_item.right_image_preview)
        self.pane.show()

    @pyqtSlot()
    def listDeleteEvent(self):
        if self.pair_list.currentItem() is not None:
            self.pair_list.takeItem(self.pair_list.row(self.pair_list.selectedItems()[0]))

    @pyqtSlot()
    def listRenameEvent(self):
        if self.pair_list.currentItem() is not None:
            self.pair_list.currentItem().rename(self.renaming_input.text())

    # Slots from custom signals do not need (or work with) pyqtSlot decorator
    def imageUploaded(self, path, button):
        selected_item = self.pair_list.currentItem()
        selected_item.load_image(path, button)

# Additional composite widgets for the main window only
class ImageUpload(QWidget):

    imageUploaded = pyqtSignal(str, QWidget)

    def __init__(self, parent, text):
        super().__init__()
        self.parent = parent

        self.content = QVBoxLayout()
        self.setLayout(self.content)
        self.label = QLabel()
        self.label.setText(text)
        self.isLeft = text == "Left view:"
        self.button = QPushButton()
        # An arbitrary size that I like, but this prevents the widgets from reflowing on image upload
        self.button.setMaximumSize(217, 180)
        self.button.setMinimumSize(217, 180)
        previewSize = self.button.size()
        previewSize = QSize(previewSize.height() - 50, previewSize.width() - 50)
        self.button.setIconSize(previewSize)
        self.button.clicked.connect(self.uploadImage)
        self.content.addWidget(self.label)
        self.content.addWidget(self.button)
        self.clearImage()

        self.imageUploaded.connect(self.parent.parent.imageUploaded)

    @pyqtSlot()
    def uploadImage(self):
        fileSelect = QFileDialog.getOpenFileName(filter=CV_SUPPORTED_FORMATS_FILTER)
        path = fileSelect[0]
        if path == "":
            return
        self.imageUploaded.emit(path, self)

    @pyqtSlot()
    def updateImage(self, icon):
        if icon is None:
            self.clearImage()
            return
        self.button.setIcon(icon)

    @pyqtSlot()
    def clearImage(self):
        self.button.setIcon(QIcon("img/placeholder.png"))

class SelectionPane(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # Init content
        self.setMaximumWidth(500)
        size_policy = QSizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)
        self.setFrameStyle(0x16) # Plain, Styled
        self.content = QVBoxLayout()
        self.setLayout(self.content)
        self.stereo_pair_layout = QHBoxLayout()
        self.output_layout = QHBoxLayout()
        self.content.addLayout(self.stereo_pair_layout)
        self.content.addLayout(self.output_layout)

        # Top half - stereo pair upload
        self.left_upload = ImageUpload(self, "Left view:")
        self.right_upload = ImageUpload(self, "Right view:")
        self.stereo_pair_layout.addWidget(self.left_upload)
        self.stereo_pair_layout.addWidget(self.right_upload)

        # Bottom half - output
        self.compute_disparity_button = QPushButton()
        self.view_disparity_button = QPushButton()
        self.view_stereo_button = QPushButton()
        self.map_interaction_layout = QVBoxLayout()
        self.map_display_frame = QFrame()
        self.map_display_layout = QVBoxLayout()
        self.map_display_frame.setLayout(self.map_display_layout)
        self.map_display_frame.setFrameStyle(0x33) # Sunken, Winpanel
        self.disparity_map_label = QLabel()
        self.disparity_map_preview = QLabel()
        button_top_spacer = QSpacerItem(0, 10)
        button_compress_spacer = QSpacerItem(0, 90)
        output_horizontal_spacer = QSpacerItem(10, 0)

        self.map_interaction_layout.addSpacerItem(button_top_spacer)
        self.map_interaction_layout.addWidget(self.compute_disparity_button)
        self.map_interaction_layout.addWidget(self.view_disparity_button)
        self.map_interaction_layout.addWidget(self.view_stereo_button)
        self.map_interaction_layout.addSpacerItem(button_compress_spacer)
        self.map_display_layout.addWidget(self.disparity_map_label)
        self.map_display_layout.addWidget(self.disparity_map_preview)

        self.output_layout.addLayout(self.map_interaction_layout)
        self.output_layout.addSpacerItem(output_horizontal_spacer)
        self.output_layout.addWidget(self.map_display_frame)

        self.compute_disparity_button.setText("Compute disparity map")
        self.view_disparity_button.setText("View disparity map")
        self.view_stereo_button.setText("View 3D scene")
        self.disparity_map_label.setText("Disparity map:")
        placeholder_disparity = QPixmap("img/placeholder.png")
        placeholder_disparity = placeholder_disparity.scaledToWidth(200)
        self.disparity_map_preview.setPixmap(placeholder_disparity)

        # Signals and slots
        self.compute_disparity_button.clicked.connect(self.compute_disparity_map)

        self.hide()

    def compute_disparity_map(self):
        # Proof of concept: this is slow and should actually open a window to configure API
        # and then start a worker to do the computation like with image upload. Need to read up more
        # on this cv library before investing effort into that lmao TODO
        a = self.parent.pair_list.currentItem()
        stereo = cv.StereoSGBM_create(numDisparities=32, blockSize=15,)
        l = cv.cvtColor(a.left_image_cv, cv.COLOR_BGR2GRAY)
        r = cv.cvtColor(a.right_image_cv, cv.COLOR_BGR2GRAY)
        disparity = stereo.compute(l, r)
        plt.imshow(disparity,'gray')
        plt.show()