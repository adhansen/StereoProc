from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow, QPushButton,
                             QListWidget, QListWidgetItem, QLineEdit, QSpacerItem, QSizePolicy)
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
        self.left_column.setMaximumWidth(250)
        self.left_column_layout = QVBoxLayout()
        self.left_column.setLayout(self.left_column_layout)

        # Left column user widgets
        self.pair_list_label = QLabel(self)
        self.pair_list = QListWidget(self)
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

        # Init user widgets
        # Left
        self.pair_list_label.setText("Stereo pairs:")
        self.renaming_button.setText("Rename")
        self.add_pair_button.setText("Add")
        self.delete_pair_button.setText("Delete")

        a = QListWidgetItem()
        a.setText("Hello List")
        b = QListWidgetItem()
        b.setText("Woahwowoowow")
        self.pair_list.addItem(a)
        self.pair_list.addItem(b) # Great, now subclass QListWidget?. I want a counter so that I never add multiple "New item (1)" which is the case if using size

        self.pane = SelectionPane()

        self.content.addWidget(self.left_column)
        self.content.addWidget(self.pane)

class ImageUpload(QWidget):
    def __init__(self, text):
        super().__init__()
        self.content = QVBoxLayout()
        self.setLayout(self.content)

        self.label = QLabel()
        self.label.setText(text)
        self.button = QPushButton()
        self.button.setFixedHeight(180)
        self.update_preview("img/placeholder.png")

        self.content.addWidget(self.label)
        self.content.addWidget(self.button)
        return
    
    def update_preview(self, path):
        self.preview = QIcon(path) #FIXME don't use this tiny-ass icon it looks like shit
        self.button.setIcon(self.preview)
        return

class SelectionPane(QFrame):
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(500)
        size_policy = QSizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)
        self.setFrameStyle(0x33)
        self.content = QVBoxLayout()
        self.setLayout(self.content)
        self.stereo_pair_layout = QHBoxLayout()
        self.output_layout = QHBoxLayout()
        self.content.addLayout(self.stereo_pair_layout)
        self.content.addLayout(self.output_layout)

        # Top half - stereo pair upload
        self.left_upload = ImageUpload("Left view:")
        self.right_upload = ImageUpload("Right view:")
        self.stereo_pair_layout.addWidget(self.left_upload)
        self.stereo_pair_layout.addWidget(self.right_upload)

        # Bottom half - output
        self.compute_disparity_button = QPushButton()
        self.view_disparity_button = QPushButton()
        self.view_stereo_button = QPushButton()
        self.map_interaction_layout = QVBoxLayout()
        self.map_display_layout = QVBoxLayout()
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
        

        self.compute_disparity_button.setText("Compute disparity map")
        self.view_disparity_button.setText("View disparity map")
        self.view_stereo_button.setText("View 3D scene")
        self.disparity_map_label.setText("Disparity map:")
        placeholder_disparity = QPixmap("img/placeholder.png")
        placeholder_disparity = placeholder_disparity.scaledToWidth(200)
        self.disparity_map_preview.setPixmap(placeholder_disparity)

        self.output_layout.addLayout(self.map_interaction_layout)
        self.output_layout.addSpacerItem(output_horizontal_spacer)
        self.output_layout.addLayout(self.map_display_layout)

       # TODO show hide based on list event(Try to keep frame sunken?), add label with pair name bolded at top