import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
import requests

secwin = uic.loadUiType("youtubeviewer.ui")[0]

class secwindow(QWidget, secwin):
    def __init__(self, url):
        try:
            super().__init__()
            self.setWindowTitle('유튜브')
            self.video_widget = QWebEngineView(self)
            self.video_widget.setUrl(QUrl(url))
            self.video_widget.setFixedSize(1280, 800)


        except Exception as e:
            print(e)





if __name__ == "__main__" :
    app = QApplication(sys.argv) #프로그램을 실행

    myWindow = secwindow()#WindowClass의 객체 생성
    myWindow.show()#프로그램 화면을 보여주는 코드
    app.exec_()#프로그램을 작동시키는 코드