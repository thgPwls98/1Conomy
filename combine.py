import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy
from PyQt5 import uic
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests
import os


# 코드 생략

API_KEY = os.getenv("YOUTUBE_API_KEY")


class YouTubeSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setupUi(self)
        self.show()
        #self.init_ui()

    # Existing methods from Ui_Form class
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(482, 824)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet("background-color: rgb(184, 229, 224);")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 461, 781))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.BtnSrch = QtWidgets.QPushButton(self.tab)
        self.BtnSrch.setGeometry(QtCore.QRect(370, 20, 71, 41))
        self.BtnSrch.setObjectName("BtnSrch")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 361, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.textBrowserLaw = QtWidgets.QTextBrowser(self.tab)
        self.textBrowserLaw.setGeometry(QtCore.QRect(20, 120, 411, 241))
        self.textBrowserLaw.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textBrowserLaw.setObjectName("textBrowserLaw")
        self.labelLaw = QtWidgets.QLabel(self.tab)
        self.labelLaw.setGeometry(QtCore.QRect(30, 90, 64, 15))
        self.labelLaw.setObjectName("labelLaw")
        self.textBrowserEx = QtWidgets.QTextBrowser(self.tab)
        self.textBrowserEx.setGeometry(QtCore.QRect(20, 450, 411, 241))
        self.textBrowserEx.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textBrowserEx.setObjectName("textBrowserEx")
        self.labelEx = QtWidgets.QLabel(self.tab)
        self.labelEx.setGeometry(QtCore.QRect(30, 420, 64, 15))
        self.labelEx.setObjectName("labelEx")
        self.btnMoreLaw = QtWidgets.QPushButton(self.tab)
        self.btnMoreLaw.setGeometry(QtCore.QRect(330, 370, 93, 28))
        self.btnMoreLaw.setObjectName("btnMoreLaw")
        self.btnMoreEx = QtWidgets.QPushButton(self.tab)
        self.btnMoreEx.setGeometry(QtCore.QRect(330, 700, 93, 28))
        self.btnMoreEx.setObjectName("btnMoreEx")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.Btnsrch = QtWidgets.QPushButton(self.tab_2)
        self.Btnsrch.setGeometry(QtCore.QRect(370, 20, 71, 41))
        self.Btnsrch.setObjectName("Btnsrch")
        self.lineEdit_srch = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_srch.setGeometry(QtCore.QRect(10, 20, 361, 41))
        self.lineEdit_srch.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_srch.setObjectName("lineEdit_srch")
        self.lineEdit_age = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_age.setGeometry(QtCore.QRect(60, 70, 61, 31))
        self.lineEdit_age.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_age.setObjectName("lineEdit_age")
        self.listWidget = QtWidgets.QListWidget(self.tab_2)
        self.listWidget.setGeometry(QtCore.QRect(10, 210, 431, 521))
        self.listWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(20, 75, 31, 21))
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 110, 173, 79))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox_plcy = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_plcy.setObjectName("comboBox_plcy")
        self.horizontalLayout.addWidget(self.comboBox_plcy)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBox_edu = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_edu.setObjectName("comboBox_edu")
        self.horizontalLayout_3.addWidget(self.comboBox_edu)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.comboBox_reg = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_reg.setObjectName("comboBox_reg")
        self.horizontalLayout_4.addWidget(self.comboBox_reg)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.layoutWidget1 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(220, 110, 173, 51))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.comboBox_emp = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBox_emp.setObjectName("comboBox_emp")
        self.horizontalLayout_6.addWidget(self.comboBox_emp)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.comboBox_spec = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBox_spec.setObjectName("comboBox_spec")
        self.horizontalLayout_5.addWidget(self.comboBox_spec)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab_2, "")


        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab_3)
        self.scrollArea_2.setGeometry(QtCore.QRect(10, 70, 431, 661))
        self.scrollArea_2.setStyleSheet("")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 429, 659))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalScrollBar_2 = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_2)
        self.verticalScrollBar_2.setGeometry(QtCore.QRect(410, 10, 16, 641))
        self.verticalScrollBar_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_2.setObjectName("verticalScrollBar_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.pushButton = QtWidgets.QPushButton('검색', self.tab_3)
        self.pushButton.setGeometry(QtCore.QRect(370, 10, 71, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.search_youtube)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 10, 361, 41))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.tabWidget.addTab(self.tab_3, "")


        keyword_layout = QHBoxLayout()
        keyword_layout.addWidget(self.lineEdit_2)
        keyword_layout.addWidget(self.pushButton)

        self.result_layout = QVBoxLayout()

        scrollArea_2 = QtWidgets.QScrollArea(self.tab_3)
        scrollArea_2.setWidgetResizable(True)
        scrollAreaWidgetContents_2 = QWidget(self.scrollArea_2)
        scrollAreaWidgetContents_2.setLayout(self.result_layout)
        scrollArea_2.setWidget(scrollAreaWidgetContents_2)                

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(keyword_layout)
        main_layout.addWidget(scrollArea_2)
        widget_layout=QVBoxLayout(self.tab_3)
        widget_layout.addLayout(main_layout)


        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.BtnSrch.setText(_translate("Form", "검색"))
        self.labelLaw.setText(_translate("Form", "법"))
        self.labelEx.setText(_translate("Form", "예시"))
        self.btnMoreLaw.setText(_translate("Form", "더보기"))
        self.btnMoreEx.setText(_translate("Form", "더보기"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "계약"))
        self.Btnsrch.setText(_translate("Form", "검색"))
        self.label.setText(_translate("Form", "나이"))
        self.label_2.setText(_translate("Form", "분야"))
        self.label_3.setText(_translate("Form", "교육상태"))
        self.label_4.setText(_translate("Form", "지역"))
        self.label_6.setText(_translate("Form", "취업상태"))
        self.label_5.setText(_translate("Form", "특화분야"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "정책"))
        self.pushButton.setText(_translate("Form", "검색"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "요리 TIP"))

    def search_youtube(self):
        if not API_KEY:
            QtWidgets.QMessageBox.warning(self, "API key missing", "Set the YOUTUBE_API_KEY environment variable.")
            return

        keyword = self.lineEdit_2.text()

        base_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': keyword,
            'maxResults': 10,
            'key': API_KEY
        }

        response = requests.get(base_url, params=params)
        results = response.json().get('items', [])

        if not results:
            self.add_result_widget('No results found.')
            return

        for result in results:
            video_id = result['id']['videoId']
            video_info = self.get_video_info(video_id)
            self.a



    def get_video_info(self, video_id):
        base_url = 'https://www.googleapis.com/youtube/v3/videos'

    params = {
        'part': 'snippet',
        'id': video_id,
        'key': API_KEY
    }

    response = requests.get(base_url, params=params)
    video_info = response.json().get('items', [])

    if not video_info:
        return {}

    snippet = video_info[0].get('snippet', {})
    video_id = video_info[0].get('id', '')
    snippet['videoId'] = video_id

    return snippet

    def add_result_widget(self, video_info):
        if video_info == 'No results found.':
            label = QLabel(video_info)
            self.result_layout.addWidget(label)
        else:
            video_id = video_info['videoId']
            title = video_info.get('title', 'N/A')


            video_widget = QWebEngineView(self)
            video_widget.setUrl(QUrl(f'https://www.youtube.com/embed/{video_id}'))
            video_widget.setFixedSize(400, 250)
            #video_widget.setAlignment(Qt.AlignTop)

            title_label = QLabel(title)
            #title_label.setFixedSize(300,400)
            title_label.setWordWrap(True)
            title_label.setAlignment(Qt.AlignTop)
            font = title_label.font()
            font.setPointSize(10)
            title_label.setFont(font)

            widget_layout = QHBoxLayout()
            widget_layout.addWidget(video_widget)
            #widget_layout.addWidget(title_label)
            widget_layout.setAlignment(Qt.AlignTop)

            widget = QWidget(self)
            widget.setLayout(widget_layout)

            self.result_layout.addWidget(widget)
            #self.scrollArea_2.addLayout(self.result_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = YouTubeSearchApp()
    sys.exit(app.exec_())