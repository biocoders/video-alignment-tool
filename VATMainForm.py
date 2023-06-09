import sys
import VATFunctions as VAT
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QFileDialog
)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    inputFilename = ""
    inputVideo = None
    transformedVideo = None
    videoWidgetInput = None
    videoWidgetTransformed = None
    videoPlayerInput = None

    def __getFileIOPanel__(self, label, defaultValue, fileMode):
        filePanel = QHBoxLayout()
        
        fileNamePanel = QVBoxLayout()
        fileNamePanel.addWidget(QLabel(label))
        editBox = QLineEdit(defaultValue)
        fileNamePanel.addWidget(editBox)
        
        filePanel.addLayout(fileNamePanel)
        btnLoad = QPushButton("Load")
        filePanel.addWidget(btnLoad)
        btnLoad.clicked.connect(lambda: self.__openFile__(editBox))
        filePanel.addWidget(QPushButton(fileMode))
        return filePanel
    
    def __openFile__(self, editBox):
        fileName, _ = QFileDialog.getOpenFileName(self, "","","Video files (*.mp4)" )
        if fileName:
            self.inputFilename = fileName
            editBox.setText(fileName)
            self.videoPlayerInput.setMedia(fileName)
            self.videoWidgetInput.show()

    def __moveToPosition__(self, pos):
        vat = VAT.VideoAlignment(self.inputFilename)
        vat.DisplayFrame(pos)


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Alignment Tool")

        mainLayout = QVBoxLayout()

        inputFilePanel = self.__getFileIOPanel__("Input Video", "", "Load")
        mainLayout.addLayout(inputFilePanel)

        videoPanel = QHBoxLayout()
        videoPanelLeft = QVBoxLayout()
        videoPanelLeft.addWidget(QLabel("Example Image"))
        self.videoWidgetInput = QVideoWidget()
        self.videoPlayerInput = QMediaPlayer()
        self.videoPlayerInput.setVideoOutput(self.videoWidgetInput)
        videoPanelLeft.addWidget(self.videoWidgetInput)
        slider = QSlider(Qt.Horizontal)
        videoPanelLeft.addWidget(slider)
        slider.sliderMoved.connect(lambda: self.__moveToPosition__(slider.pos))
        videoPanel.addLayout(videoPanelLeft)

        videoPanelRight = QVBoxLayout()
        videoPanel.addLayout(videoPanelRight)
        
        mainLayout.addLayout(videoPanel)

        outputFilePanel = self.__getFileIOPanel__("Output Video", "", "Save")
        mainLayout.addLayout(outputFilePanel)

        widget = QWidget()
        widget.setLayout(mainLayout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()