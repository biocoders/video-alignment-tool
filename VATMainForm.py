import sys
import VATFunctions as VAT
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
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
    imageWidgetInput = None
    imageWidgetOutput = None
    vat = None
    inputEditBox = None
    transformedEditBox = None

    def __openFile__(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "","","Video files (*.mp4)" )
        if fileName:
            self.inputFilename = fileName
            self.inputEditBox.setText(fileName)
            self.vat.SetVideo(fileName)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.mediaPlayer.pause()

    def __moveToPosition__(self, pos):
        self.imageWidgetInput.load(self.vat.GetFrame(pos))


    def __init__(self):
        super().__init__()
        self.vat = VAT.VideoAlignment("")
        self.setWindowTitle("Video Alignment Tool")
        self.setFixedHeight(600)
        self.setFixedWidth(800)

        mainLayout = QVBoxLayout()

        inputFilePanel = QHBoxLayout()
        fileNamePanel = QVBoxLayout()
        fileNamePanel.addWidget(QLabel("Input Video"))
        self.inputEditBox  = QLineEdit()
        fileNamePanel.addWidget(self.inputEditBox)

        inputFilePanel.addLayout(fileNamePanel)
        btnLoad = QPushButton("Open")
        inputFilePanel.addWidget(btnLoad)
        btnLoad.clicked.connect(lambda: self.__openFile__())
        inputFilePanel.addWidget(QPushButton("Load"))


        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(videoWidget)
        inputFilePanel.addWidget(videoWidget)

        mainLayout.addLayout(inputFilePanel)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()