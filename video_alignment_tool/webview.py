'''
pip install PyQt6 PyQt6-WebEngine
'''
import PyQt6
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIntValidator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Behavioral Video Alignment Tool")
        # view = View()
        webview = QWebEngineView()
        webview.settings().setAttribute(webview.settings().WebAttribute.PluginsEnabled, True)
        webview.settings().setAttribute(webview.settings().WebAttribute.PdfViewerEnabled, True)
        page = QWebEnginePage()
        # webview.setPage(page)
        url = QtCore.QUrl.fromLocalFile('file:///Users/andretelfer/repos/video-alignment-tool/cv4animals_mouse-irl.pdf')
        webview.setUrl(url)
        # page.load(QtCore.QUrl())
        self.setCentralWidget(webview)

# from PyQt6.QtCore import QUrl
# from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
# from PyQt6.QtWebEngineWidgets import QWebEngineView #, QWebEngineSettings
# from os import path

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(QMainWindow, self).__init__()

#         self.setWindowTitle("PDF Viewer")
#         self.setGeometry(0, 28, 1000, 750)

#         self.webView = QWebEngineView()
#         self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PluginsEnabled, True)
#         self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PdfViewerEnabled, True)
#         self.setCentralWidget(self.webView)

#     def url_changed(self):
#         self.setWindowTitle(self.webView.title())

#     def go_back(self):
#         self.webView.back()

# if __name__ == '__main__':

#     import sys
#     app = QApplication(sys.argv)
#     win = MainWindow()
#     win.show()
#     if len(sys.argv) > 1:
#         win.webView.setUrl(QUrl(f"file://{sys.argv[1]}"))
#     else:
#         wd = path.dirname(path.abspath(sys.argv[0]))
#         test_pdf = "test.pdf"
#         win.webView.setUrl(QUrl(f"file://{wd}/{test_pdf}"))
#     sys.exit(app.exec())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()