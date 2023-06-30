import PyQt6
import sys
import numpy as np

from matplotlib.figure import Figure
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

CONTROL_COLUMN_WIDTH = 200

class ControlColumnWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(CONTROL_COLUMN_WIDTH)
        self.setContentsMargins(0,0,0,0)

class TransformedFrameDisplayWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=6, height=2, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = self.fig.add_subplot(111)
        dummy_image = np.zeros(shape=(1,1,3), dtype=np.uint8)
        self.image = self.axes.imshow(dummy_image)
        self.axes.legend(loc='upper right')
        self.axes.grid()
        super().__init__(self.fig)

class VideoFrameDisplayWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=6, height=2, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = self.fig.add_subplot(111)
        dummy_image = np.zeros(shape=(1,1,3), dtype=np.uint8)
        self.image = self.axes.imshow(dummy_image)
        self.axes.legend(loc='upper right')
        self.axes.grid()
        super().__init__(self.fig)
        self.setContentsMargins(0,0,0,0)

class View(QWidget):
    def __init__(self):
        super().__init__()
        
        # Setup the basic layout
        layout = QVBoxLayout()
        layout.addLayout(self.input_file_section())
        layout.addLayout(self.video_registration_section())
        self.setLayout(layout)

    def input_file_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)

        label = QLabel("Input Video")
        label.setContentsMargins(0,0,0,0)
        label.setFixedHeight(12)
        layout.addWidget(label)

        hlayout = QHBoxLayout()
        input_field = QLineEdit()
        hlayout.addWidget(input_field)

        controls = ControlColumnWidget()
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(0)
        controls.setFixedHeight(50)
        controls.setLayout(controls_layout)
        controls.setFixedWidth(CONTROL_COLUMN_WIDTH)

        browse_button = QPushButton("Browse")
        controls_layout.addWidget(browse_button)

        load_button = QPushButton("Load")
        controls_layout.addWidget(load_button)
        
        hlayout.addWidget(controls)
        layout.addLayout(hlayout)
        return layout

    def video_registration_section(self):
        hlayout = QHBoxLayout()

        # Setup the left column
        left_widget = QWidget()
        left_column = QVBoxLayout()
        label = QLabel("Original Video")
        slider = QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        video_frame_widget = VideoFrameDisplayWidget()
        left_column.addWidget(label, stretch=0)
        left_column.addWidget(video_frame_widget, stretch=1)
        left_column.addWidget(slider, stretch=0)

        left_widget.setLayout(left_column)
        hlayout.addWidget(left_widget)

        # Create the right column
        controls = ControlColumnWidget()
        controls.setContentsMargins(0,0,0,0)
        controls_layout = QVBoxLayout()
        label = QLabel("Registration Points")

        table = QTableWidget(4,2)
        for i in range(4):
            for j in range(2):
                item = QTableWidgetItem("0.0")
                table.setItem(i,j,item)

        table.setHorizontalHeaderLabels(["x", "y"])
        table.setVerticalHeaderLabels(["p0", "p1", "p2", "p3"])
        header = table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        table.show()

        controls_layout.addWidget(label, stretch=0) 
        controls_layout.addWidget(table, stretch=1)
        controls.setLayout(controls_layout)
        hlayout.addWidget(controls)
        return hlayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Behavioral Video Alignment Tool")
        view = View()
        self.setCentralWidget(view)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()