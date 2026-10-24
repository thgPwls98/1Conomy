
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import ssl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import webbrowser
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from uitest import WindowClass


start = uic.loadUiType("start.ui")[0]

class startwindow(QMainWindow, start):
    def __init__(self):
        self.pixmap = QPixmap("startimg.png")
        super().__init__()
        self.setupUi(self)
        self.imglbl.setPixmap(self.pixmap)
        self.imglbl.resize(self.pixmap.width(), self.pixmap.height())
        self.imglbl.move(int(self.width() / 2) - int(self.imglbl.width()/2), int(self.height() / 2) - int(self.imglbl.height()/2) -130)
        self.btnstart.clicked.connect(self.clicked_start)
        self.setWindowIcon(QIcon('1conomy.png'))

    def clicked_start(self):
        try:
            self.hide()
            self.window = WindowClass()
            self.window.show()
        except Exception as e:
            print(e)

if __name__ == "__main__" :
    app = QApplication(sys.argv) #프로그램을 실행
    myWindow = startwindow()#WindowClass의 객체 생성
    myWindow.show()#프로그램 화면을 보여주는 코드
    app.exec_()#프로그램을 작동시키는 코드