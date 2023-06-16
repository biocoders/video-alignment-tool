import sys
from types import LambdaType

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QSlider,
)

def test_click():
        print("omg it works")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        
        self.setFixedWidth(1200)
        self.setFixedHeight(800)

        pagelayout = QVBoxLayout()
        load_layout = QHBoxLayout()
        video_layout = QVBoxLayout()
        coordinate_layout= QHBoxLayout()
        coordinate_layout2= QHBoxLayout()
        video_transformed_layout= QVBoxLayout()
        export_layout= QHBoxLayout()
       
       

        pagelayout.addLayout(load_layout)
        pagelayout.addLayout(video_layout)
        pagelayout.addLayout(coordinate_layout)
        pagelayout.addLayout(coordinate_layout2)
        pagelayout.addLayout(video_transformed_layout)
        pagelayout.addLayout(export_layout)
        

        ####### Load Video layout
        path= QLabel()
        load= QPushButton()
        open= QPushButton()
        load.setText("LOAD")
        open.setText("OPEN")
        path.setText("path/to/file")

        load_layout.addWidget(path)
        load_layout.addWidget(load)
        load_layout.addWidget(open)

        ######### VIDEO LAYOUT ###################
        pixmap = QPixmap('/Users/matthieuvilain/Desktop/Student_visa/headshot.jpeg')
        video= QLabel()
        video.setScaledContents(True)
        video.setPixmap(pixmap)
        video_layout.addWidget(video)
        slider= QSlider(Qt.Horizontal, self)
        video_layout.addWidget(slider)

    
        

        ##########@ SLIDER and BUTTON LAYOUT ##########
        x1= QLineEdit()
        x2= QLineEdit()
        x3= QLineEdit()
        x4= QLineEdit()
        x1.setText("X1")
        x2.setText("X2")
        x3.setText("X3")
        x4.setText("X4")
        coordinate_layout.addWidget(x1)
        coordinate_layout.addWidget(x2)
        coordinate_layout.addWidget(x3)
        coordinate_layout.addWidget(x4)

        y1= QLineEdit()
        y2= QLineEdit()
        y3= QLineEdit()
        y4= QLineEdit()
        y1.setText("X1")
        y2.setText("X2")
        y3.setText("X3")
        y4.setText("X4")
        coordinate_layout2.addWidget(y1)
        coordinate_layout2.addWidget(y2)
        coordinate_layout2.addWidget(y3)
        coordinate_layout2.addWidget(y4)

        ######### TRANSFORM VIDEO LAYOUT ##############
        pixmap = QPixmap('/Users/matthieuvilain/Desktop/Student_visa/headshot.jpeg')
        label= QLabel()
        label.setScaledContents(True)
        label.setPixmap(pixmap)
        video_transformed_layout.addWidget(label)

        ######### EXPORT LAYOUT ##############
        refresh= QPushButton()
        refresh.setCheckable(True)
        refresh.clicked.connect(self.test_clicked)
        save= QPushButton()
        refresh.setText("REFRESH")
        save.setText("SAVE")

        export_layout.addWidget(refresh)
        export_layout.addWidget(save)

        ###### FINAL SET UP ###########
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
    
    def test_clicked(self):
        test_click()
        


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()