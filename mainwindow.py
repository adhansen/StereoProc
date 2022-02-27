from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow, QPushButton,
                             QListWidget, QListWidgetItem, QLineEdit, QSpacerItem)
from PyQt5.QtGui import (QIcon, QPixmap)

from pairmodelview import (PairPreview)

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
        self.middle_column = QWidget()
        self.right_column = QWidget()
        self.left_column.setMaximumWidth(250)
        self.middle_column.setMaximumWidth(250)
        self.right_column.setMaximumWidth(250)
        self.left_column_layout = QVBoxLayout()
        self.middle_column_layout = QVBoxLayout()
        self.right_column_layout = QVBoxLayout()
        self.left_column.setLayout(self.left_column_layout)
        self.middle_column.setLayout(self.middle_column_layout)
        self.right_column.setLayout(self.right_column_layout)

        # Left column user widgets
        self.pair_list_label = QLabel(self)
        self.pair_list = QListWidget(self)
        self.list_button_layout = QHBoxLayout()
        self.add_pair_button = QPushButton(self)
        self.delete_pair_button = QPushButton(self)

        self.list_button_layout.addWidget(self.add_pair_button)
        self.list_button_layout.addWidget(self.delete_pair_button)
        self.left_column_layout.addWidget(self.pair_list_label)
        self.left_column_layout.addWidget(self.pair_list)
        self.left_column_layout.addLayout(self.list_button_layout)

        # Center column user widgets
        self.renaming_layout = QHBoxLayout()
        self.renaming_input = QLineEdit(self)
        self.renaming_button = QPushButton(self)
        self.renaming_layout.addWidget(self.renaming_input)
        self.renaming_layout.addWidget(self.renaming_button)

        self.label_left_eye = QLabel()
        self.left_eye_button = ImageUploadButton()
        self.label_right_eye = QLabel()
        self.right_eye_button = ImageUploadButton()

        self.middle_column_layout.addLayout(self.renaming_layout)
        self.middle_column_layout.addWidget(self.label_left_eye)
        self.middle_column_layout.addWidget(self.left_eye_button)
        self.middle_column_layout.addWidget(self.label_right_eye)
        self.middle_column_layout.addWidget(self.right_eye_button)

        # Right column user widgets
        self.disparity_map_label = QLabel()
        self.disparity_map_preview = QLabel()
        self.compute_disparity_button = QPushButton()
        self.view_disparity_button = QPushButton()
        self.view_stereo_button = QPushButton()
        self.right_column_spacer = QSpacerItem(0, 175)

        self.right_column_layout.addWidget(self.compute_disparity_button)
        self.right_column_layout.addWidget(self.view_disparity_button)
        self.right_column_layout.addWidget(self.view_stereo_button)
        self.right_column_layout.addWidget(self.disparity_map_label)
        self.right_column_layout.addWidget(self.disparity_map_preview)
        self.right_column_layout.addSpacerItem(self.right_column_spacer)

        # Init user widgets
        # Left
        self.pair_list_label.setText("Stereo pairs:")
        self.add_pair_button.setText("Add")
        self.delete_pair_button.setText("Delete")
        # Center
        self.renaming_button.setText("Rename")
        self.label_left_eye.setText("Left view:")
        self.label_right_eye.setText("Right view:")
        # Right
        self.compute_disparity_button.setText("Compute disparity map")
        self.view_disparity_button.setText("View disparity map")
        self.view_stereo_button.setText("View 3D scene")
        self.disparity_map_label.setText("Disparity map:")
        placeholder_disparity = QPixmap("img/placeholder.png")
        placeholder_disparity = placeholder_disparity.scaledToWidth(200)
        self.disparity_map_preview.setPixmap(placeholder_disparity)

        a = QListWidgetItem()
        a.setText("Hello List")
        b = QListWidgetItem()
        b.setText("Woahwowoowow")
        self.pair_list.addItem(a)
        self.pair_list.addItem(b) # Great, now subclass QListWidget?. I want a counter so that I never add multiple "New item (1)" which is the case if using size

        self.content.addWidget(self.left_column)
        self.content.addWidget(self.middle_column)
        self.content.addWidget(self.right_column)

class ImageUploadButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(180)
        self.update_preview("img/placeholder.png")
        return
    
    def update_preview(self, path):
        self.preview = QIcon(path) #FIXME don't use this tiny-ass icon it looks like shit
        self.setIcon(self.preview)
        return
