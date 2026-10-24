import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QScrollArea, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import requests
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # .ui 파일에서 UI를 로드합니다.
        uic.loadUi('main.ui', self)

        self.pushButton.clicked.connect(self.search_and_play_videos)

    def search_and_play_videos(self):
        if not API_KEY:
            QMessageBox.warning(self, "API key missing", "Set the YOUTUBE_API_KEY environment variable.")
            return

        # QTextEdit에서 키워드를 가져옵니다.
        keyword = self.textEdit_2.toPlainText()

        # YouTube API를 사용하여 동영상 검색
        base_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': keyword,
            'type': 'video',
            'maxResults': 10,
            'key': API_KEY  # 여러분의 YouTube API 키로 교체하세요
        }

        response = requests.get(base_url, params=params)
        results = response.json().get('items', [])

        # 스크롤 영역의 이전 콘텐츠를 지웁니다.
        content_widget = self.scrollArea_2.widget()
        
        if content_widget.layout() is None:
            content_layout = QVBoxLayout(content_widget)
        else:
            content_layout = content_widget.layout()
            
        for i in reversed(range(content_layout.count())):
            content_layout.itemAt(i).widget().setParent(None)

        # 스크롤 영역에 동영상 위젯을 추가합니다.
        for result in results:
            video_id = result.get('id', {}).get('videoId', None)
            if video_id:
                video_widget = QWebEngineView()
                video_widget.setUrl(QUrl(f'https://www.youtube.com/embed/{video_id}'))
                video_widget.setFixedSize(400, 225)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
