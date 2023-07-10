"""

Documentation:
- BoxModel: https://doc.qt.io/qt-6/stylesheet-customizing.html#the-box-model
- 
"""

import PyQt6
import sys
import numpy as np

from matplotlib.figure import Figure
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QIntValidator
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

DEBUG = False

GLOBAL_STYLES = """
QLabel {
    min-height: 10px;
    max-height: 10px;
    font-size: 10px; 
    margin-bottom: 3px;
}

.ControlsColumn {
    min-width: 240px;
    max-width: 240px;
}
"""

class EmptyQVBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)

class EmptyQHBoxLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
    
class MatplotlibFigureWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=6, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = self.fig.add_subplot(111)

        dummy_image = np.zeros(shape=(100,100,3), dtype=np.uint8)
        self.image = self.axes.imshow(dummy_image)
        self.axes.set_aspect('equal')
        # self.axes.legend(loc='upper right')
        self.axes.grid()
        super().__init__(self.fig)

class VideoSelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Define widgets
        label = QLabel("VIDEO INPUT")
        filepath_input = QLineEdit()
        filepath_input.setPlaceholderText("/path/to/video.mp4")
        browse_button = QPushButton("Browse")
        load_button = QPushButton("Load")

        # Layout
        layout = EmptyQVBoxLayout()
        layout.addWidget(label, stretch=0)
        hlayout = EmptyQHBoxLayout()
        hlayout.addWidget(filepath_input)
        control_widget = QWidget() # used for positioning
        control_hlayout = EmptyQHBoxLayout()
        control_hlayout.addWidget(browse_button, stretch=1)
        control_hlayout.addWidget(load_button, stretch=1)
        control_widget.setLayout(control_hlayout)
        hlayout.addSpacing(10)
        hlayout.addWidget(control_widget, stretch=0)
        layout.addLayout(hlayout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        
        # Styles 
        self.setProperty('class', 'VideoSelectionWidget')
        control_widget.setProperty('class', 'ControlsColumn')
        styles = '''
        QLabel {
            margin-bottom: 1px;
        }

        QPushButton {
            min-width: 80px;
            font-size: 10px;
        }

        QLineEdit {
            max-height: 26px;
            border: 0px;
            padding: 0px;
        }
        '''

        if DEBUG:
            styles += '''
            QWidget {
                background-color: "green";
                color: "white";
            }
            '''
        self.setStyleSheet(styles)

class RegisterPointsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Widgets
        int_val = QIntValidator()
        figure_widget = MatplotlibFigureWidget()
        figure_label = QLabel("FRAME")
        registration_label = QLabel("REGISTRATION POINTS")
        x0 = QLineEdit()
        x1 = QLineEdit()
        x2 = QLineEdit()
        x3 = QLineEdit()
        y0 = QLineEdit()
        y1 = QLineEdit()
        y2 = QLineEdit()
        y3 = QLineEdit()

        for i, w in enumerate([x0,x1,x2,x3]):
            w.setValidator(int_val)
            w.setPlaceholderText(f"x{i}")

        for i, w in enumerate([y0,y1,y2,y3]):
            w.setValidator(int_val)
            w.setPlaceholderText(f"y{i}")

        time_crop_label = QLabel("TIME CROP")
        start_frame_input = QLineEdit()
        start_frame_input.setPlaceholderText('Start Frame')
        start_frame_input.setValidator(int_val)
        stop_frame_input = QLineEdit()
        stop_frame_input.setPlaceholderText('Stop Frame')
        stop_frame_input.setValidator(int_val)

        # Layout
        layout = EmptyQHBoxLayout()
        left_widget = QWidget()
        left_widget_layout = EmptyQVBoxLayout()
        frame_layout = EmptyQHBoxLayout()
        left_widget_layout.addWidget(figure_label)
        left_widget_layout.addWidget(figure_widget)
        left_widget_layout.addLayout(frame_layout)
        left_widget.setLayout(left_widget_layout)

        right_widget = QWidget()
        right_widget_layout = EmptyQVBoxLayout()
        right_widget_layout.addWidget(registration_label)
        right_widget_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        for wx, wy in [[x0,y0], [x1,y1], [x2,y2], [x3,y3]]:
            row_layout = EmptyQHBoxLayout()
            row_layout.addWidget(wx)
            row_layout.addWidget(wy)
            right_widget_layout.addLayout(row_layout)

        right_widget_layout.addSpacing(20)
        right_widget_layout.addWidget(time_crop_label)
        row_layout = EmptyQHBoxLayout()
        row_layout.addWidget(start_frame_input)
        row_layout.addWidget(stop_frame_input)
        right_widget_layout.addLayout(row_layout)

        frame_slider = FrameSlider() #Initializing class
        self.slider = frame_slider 
        right_widget_layout.addWidget(self.slider)
        
        right_widget.setLayout(right_widget_layout)
        layout.addWidget(left_widget)
        layout.addSpacing(10)
        layout.addWidget(right_widget)
        self.setLayout(layout)

        # Styling
        right_widget.setProperty('class', 'ControlsColumn')

        frame_layout.setSpacing(5)
        styles = '''
        .FrameInput {
            max-width: 80px;
        }
        '''
        self.setStyleSheet(styles)


class FrameSlider(QWidget):
    def __init__(self):
        super().__init__()
        
        frame_slider = QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        self.slider = frame_slider
        frame_slider.valueChanged[int].connect(self.changeValue)
        frame_input = QLineEdit()
        #frame_input.setValidator(int_val)
        frame_input.setText("0")
        frame_label = QLabel('Current Frame:')
        frame_layout_v = EmptyQVBoxLayout()
        frame_layout_h = EmptyQHBoxLayout()
        frame_layout_v.addSpacing(10)
        
        frame_layout_v.addWidget(frame_slider)
        frame_layout_h.addWidget(frame_label)
        frame_layout_h.addWidget(frame_input)
        frame_input.setProperty('class', 'FrameInput')
        frame_layout_v.addLayout(frame_layout_h)
        self.setLayout(frame_layout_v)

        
    def changeValue(self):
        print(self.slider.value())
        

class ValidateRegistrationPointsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Widgets
        figure_widget = MatplotlibFigureWidget()
        figure_label = QLabel("TRANSFORMED FRAME")
        refresh_button = QPushButton("Refresh")

        # Layout
        layout = EmptyQVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(figure_label)

        hlayout = EmptyQHBoxLayout()
        hlayout.addWidget(figure_widget)
        control_widget = QWidget() # used for positioning
        control_hlayout = EmptyQVBoxLayout()
        control_hlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        control_hlayout.addWidget(refresh_button)
        control_widget.setLayout(control_hlayout)
        hlayout.addSpacing(10)
        hlayout.addWidget(control_widget)
        layout.addLayout(hlayout)
        self.setLayout(layout)

        # Styling
        control_widget.setProperty('class', 'ControlsColumn')
        styles = '''
        QPushButton {
            max-width: 120px;
            font-size: 10px;
        }
        '''
        self.setStyleSheet(styles)


class WriteVideoWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Define widgets
        label = QLabel("SAVE FOLDER")
        filepath_input = QLineEdit()
        filepath_input.setPlaceholderText("/path/to/output/directory/")
        browse_button = QPushButton("Browse")
        load_button = QPushButton("Write")

        # Layout
        layout = EmptyQVBoxLayout()
        layout.addWidget(label, stretch=0)
        hlayout = EmptyQHBoxLayout()
        hlayout.addWidget(filepath_input)
        control_widget = QWidget() # used for positioning
        control_hlayout = EmptyQHBoxLayout()
        control_hlayout.addWidget(browse_button, stretch=1)
        control_hlayout.addWidget(load_button, stretch=1)
        control_widget.setLayout(control_hlayout)
        hlayout.addSpacing(10)
        hlayout.addWidget(control_widget, stretch=0)
        layout.addLayout(hlayout)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        
        # Styles 
        self.setProperty('class', 'VideoSelectionWidget')
        control_widget.setProperty('class', 'ControlsColumn')
        styles = '''
        QLabel {
            margin-bottom: 1px;
        }

        QPushButton {
            min-width: 80px;
            font-size: 10px;
        }

        QLineEdit {
            max-height: 26px;
            border: 0px;
            padding: 0px;
        }
        '''
        self.setStyleSheet(styles)


class View(QWidget):
    def __init__(self):
        super().__init__()

        video_selection_widget = VideoSelectionWidget()
        register_points_widget = RegisterPointsWidget()
        validate_registration_points_widget = ValidateRegistrationPointsWidget()
        write_video_widget = WriteVideoWidget()

        layout = QVBoxLayout()
        layout.addWidget(video_selection_widget, stretch=0)
        layout.addSpacing(10)
        layout.addWidget(register_points_widget, stretch=53)
        layout.addSpacing(10)
        layout.addWidget(validate_registration_points_widget, stretch=47)
        layout.addSpacing(10)
        layout.addWidget(write_video_widget, stretch=0)
        self.setLayout(layout)

        styles = GLOBAL_STYLES
        self.setStyleSheet(styles)

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
