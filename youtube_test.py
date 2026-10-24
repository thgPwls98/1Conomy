import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy
from PyQt5 import uic
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

form_class = uic.loadUiType("main.ui")[0]

class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.search_youtube)

    def search_youtube(self):
        API_KEY = os.getenv("YOUTUBE_API_KEY")
        keyword = self.lineEdit_2.text()

        driver = webdriver.Chrome()  # (chrome_options)
        driver.implicitly_wait(5)
        driver.get('https://www.youtube.com/')

        driver.find_element(By.XPATH, '//*[@id="search_input"]').send_keys(keyword)
        # base_url = 'https://www.googleapis.com/youtube/v3/search'
        # params = {
        #     'part': 'snippet',
        #     'q': keyword,
        #     'maxResults': 10,
        #     'key': API_KEY
        # }
        #
        # response = requests.get(base_url, params=params)
        # results = response.json().get('items', [])
        #
        # if not results:
        #     self.add_result_widget('No results found.')
        #     return
        #
        # for result in results:
        #     video_id = result['id']['videoId']
        #     video_info = self.get_video_info(video_id)
        #     self.add_result_widget(video_info)
        #
        #     def get_video_info(self, video_id):
        #         base_url = 'https://www.googleapis.com/youtube/v3/videos'
        #         params = {
        #             'part': 'snippet',
        #             'id': video_id,
        #             'key': API_KEY
        #         }
        #
        #         response = requests.get(base_url, params=params)
        #         video_info = response.json().get('items', [])
        #
        #         if not video_info:
        #             return {}
        #
        #         snippet = video_info[0].get('snippet', {})
        #         video_id = video_info[0].get('id', '')
        #         snippet['videoId'] = video_id
        #
        #         return snippet
        #
        #     def add_result_widget(self, video_info):
        #         if video_info == 'No results found.':
        #             label = QLabel(video_info)
        #             self.result_layout.addWidget(label)
        #         else:
        #             video_id = video_info['videoId']
        #             title = video_info.get('title', 'N/A')
        #
        #             video_widget = QWebEngineView(self)
        #             video_widget.setUrl(QUrl(f'https://www.youtube.com/embed/{video_id}'))
        #             video_widget.setFixedSize(400, 250)
        #             # video_widget.setAlignment(Qt.AlignTop)
        #
        #             title_label = QLabel(title)
        #             # title_label.setFixedSize(300,400)
        #             title_label.setWordWrap(True)
        #             title_label.setAlignment(Qt.AlignTop)
        #             font = title_label.font()
        #             font.setPointSize(10)
        #             title_label.setFont(font)
        #
        #             widget_layout = QHBoxLayout()
        #             widget_layout.addWidget(video_widget)
        #             # widget_layout.addWidget(title_label)
        #             widget_layout.setAlignment(Qt.AlignTop)
        #
        #             widget = QWidget(self)
        #             widget.setLayout(widget_layout)
        #
        #             self.result_layout.addWidget(widget)
        #             # self.scrollArea_2.addLayout(self.result_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = WindowClass()
    sys.exit(app.exec_())