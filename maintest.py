
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from urllib.request import urlretrieve
from youtubeviewer import secwindow
import os

plcy = ['전체 선택', '일자리분야', '주거분야', '교육분야', '복지.문화분야', '참여.권리분야'] #콤보박스에 넣을 내용
srchreg = ['전체 선택', '중앙부처', '서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종']
emp = ['전체 선택', '재직자', '자영업자', '미취업자', '프리랜서', '일용근로자', '(예비)창업자', '단기근로자', '영농종사자', '제한없음']
edu = ['전체 선택', '고졸 미만', '고교 재학', '고졸 예정', '고교 졸업', '대학 재학', '대졸 예정', '대학 졸업', '석·박사', '제한없음']
spec = ['전체 선택', '중소기업', '여성', '저소득층', '장애인', '농업인', '군인', '지역인재', '제한없음']

srchw = '' #쿼리 설정을 위한 변수
srchp = ''
srchr = ''
srchemp = ''
srchedu = ''
srchspec = ''
srcha = ''
local_bizid = [] #정책 고유번호 저장
link1 = '' #유저가 검색한 사이트의 링크 저장
ck = 0
tempbtn = []
tempvid = []

form_class = uic.loadUiType("main2.ui")[0]
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        self.pixmap_law = QPixmap("law.png")
        self.pixmap_judge = QPixmap("judge.png")
        self.pixmap_food = QPixmap("food.png")
        super().__init__()
        self.setupUi(self)
        # self.setFixedSize(1000, 500)

        self.setWindowTitle('1인 가구 생활 지원 프로그램')
        self.imglbl_law.setPixmap(self.pixmap_law)
        self.imglbl_judge.setPixmap(self.pixmap_judge)
        self.imglbl_food.setPixmap(self.pixmap_food)
        self.imglbl_law.move(30,10)
        self.imglbl_judge.move(30, 10)
        self.imglbl_food.move(30, 10)
        self.imglbl_law.resize(self.pixmap_law.width(), self.pixmap_law.height())
        self.imglbl_food.resize(self.pixmap_law.width(), self.pixmap_law.height())
        self.imglbl_judge.resize(self.pixmap_law.width(), self.pixmap_law.height())
        self.Btnsrch.clicked.connect(self.BtnsrchFunc)  # 버튼 클릭 이벤트 생성
        self.Btnsrch.setText('검색')
        self.comboBox_plcy.addItems(plcy) # 리스트 안에 있는 내용을 콤보박스에 추가
        self.comboBox_reg.addItems(srchreg)
        self.comboBox_emp.addItems(emp)
        self.comboBox_edu.addItems(edu)
        self.comboBox_spec.addItems(spec)
        self.lineEdit.returnPressed.connect(self.btnClick)
        self.BtnSrch.clicked.connect(self.btnClick)
        self.textBrowserLaw.setOpenExternalLinks(True)
        self.textBrowserLaw.setAcceptRichText(True)
        self.textBrowserEx.setOpenExternalLinks(True)
        self.textBrowserEx.setAcceptRichText(True)
        self.setWindowIcon(QIcon('1conomy.png'))
        self.lineEdit_srch.setPlaceholderText('검색할 정책을 입력하시오.')
        self.lineEdit_2.setPlaceholderText('검색할 음식을 입력하시오.')
        self.lineEdit.setPlaceholderText('검색할 키워드을 입력하시오.')
        self.pushButton.clicked.connect(self.search_and_play_videos)
        self.stacked_widget = QStackedWidget(self.tab_3)  # QStackedWidget 생성
        self.stacked_widget.setGeometry(0, 80, 900, 300)
        self.stacked_widget.setFrameShape(QFrame.Box)

        self.show()

        self.listWidget.itemDoubleClicked.connect(self.chkItemDoubleCliked) # 리스트위젯 더블클릭 이벤트 생성

        # self.srchw = ''  # 쿼리 설정을 위한 변수
        # self.srchp = ''
        # self.srchr = ''
        # self.srchemp = ''
        # self.srchedu = ''
        # self.srchspec = ''
        # self.srcha = ''
        # self.local_bizid = []  # 정책 고유번호 저장
        # self.link1 = ''  # 유저가 검색한 사이트의 링크 저장

    def search_and_play_videos(self):
        global ck, tempbtn, tempvid
        # QTextEdit에서 키워드를 가져옵니다.
        keyword = self.lineEdit_2.text()

        # YouTube API를 사용하여 동영상 검색
        API_KEY = os.getenv("YOUTUBE_API_KEY")
        if not API_KEY:
            QMessageBox.warning(self, "API key missing", "Set the YOUTUBE_API_KEY environment variable.")
            return
        base_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': keyword,
            'type': 'video',
            'maxResults': 30,
            'key': API_KEY  # 여러분의 YouTube API 키로 교체하세요
        }

        response = requests.get(base_url, params=params)
        results = response.json().get('items', [])

        # 스크롤 영역의 이전 콘텐츠를 지웁니다.

        # content_widget = self.stacked_widget
        # try:
        #     if content_widget.layout() is None:
        #         content_layout = QGridLayout(content_widget)
        #     else:
        #         content_layout = content_widget.layout()
        #     for i in reversed(range(content_layout.count())):
        #         content_layout.itemAt(i).setParent(None)
        #
        # except Exception as e:
        #     print(e)

        # 스크롤 영역에 동영상 위젯을 추가합니다.
        # for result in results:
        #     video_id = result.get('id', {}).get('videoId', None)
        #     video_title = result.get('snippet', {}).get('title', None)
        #     video_thumbnails = result.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', None)
        #
        #     print(result)
        #     if video_id:
        #         video_widget = QWebEngineView()
        #         video_widget.setUrl(QUrl(f'https://www.youtube.com/embed/{video_id}'))
        #         video_widget.setFixedSize(400, 225)
        #         print(video_thumbnails)
        #         try:
        #             a = QGridLayout()
        #             a.addWidget(video_widget, 0, 0)
        #             a.addWidget(QLabel(f'{video_title}'), 0, 1)
        #             if i % 6 == 0 and i != 0:
        #                 page = QWidget()
        #                 page.addWidget(a)
        #             # content_layout.addWidget(video_widget)
        #             #content_layout.addWidget(QLabel(f'{video_title}'))
        #
        #         except Exception as e:
        #             print(e)
        pages = self.stacked_widget.count()
        try:
            if pages is None:
                for i in range(5):
                    button = QPushButton(f'{i + 1}', self)
                    button.clicked.connect(lambda: self.btnpage())
                    self.horizontalLayout_7.addWidget(button)
            else:
                for i in range(pages):
                        widget = self.stacked_widget.widget(0)
                        self.stacked_widget.removeWidget(widget)
                tempbtn = []
                tempvid = []

        except Exception as e:
            print(e)

        if ck == 0:
            for i in range(5):
                button = QPushButton(f'{i + 1}', self)
                button.clicked.connect(lambda: self.btnpage())
                self.horizontalLayout_7.addWidget(button)
            ck += 1


        try:
            for i in range(5):
                page = QWidget()
                grid_layout = QGridLayout(page)
                index = 0
                for row in range(2):
                    for col in range(3):
                        video_id = results[(i * 6) + index].get('id', {}).get('videoId', None)
                        video_title = results[(i * 6) + index].get('snippet', {}).get('title', None)
                        video_thumbnails = results[(i * 6) + index].get('snippet', {}).get('thumbnails', {}).get('high', {}).get('url', None)
                        folder = os.path.join('C:/Users/tahun/PycharmProjects/crawling_test/img',f'{(i * 6) + index}.png')
                        urlretrieve(video_thumbnails, folder)

                        index += 1
                        print(video_title)
                        if video_id:
                            # video_widget = QWebEngineView()
                            # video_widget.setUrl(QUrl(f'https://www.youtube.com/embed/{video_id}'))
                            # video_widget.setFixedSize(300,200)
                            a = QVBoxLayout()
                            # a.addWidget(video_widget)
                            tempvid.append((f'https://www.youtube.com/embed/{video_id}'))
                            img = QLabel()
                            a.addWidget(img)
                            pixmap_thumb = QPixmap(folder)
                            img.setPixmap(pixmap_thumb)
                            img.setScaledContents(True)
                            btnview = QPushButton(f'{video_title}')
                            tempbtn.append(btnview.text())
                            a.addWidget(btnview)
                            btnview.clicked.connect(lambda: self.btnview())
                            grid_layout.addLayout(a, row, col)
                            img.setPixmap(QPixmap(folder).scaled(img.width(), img.height()))
                self.stacked_widget.addWidget(page)

            self.stacked_widget.setCurrentIndex(0)
            print(tempbtn)
        except Exception as e:
            print(e)

    def btnview(self):
        global tempvid, tempbtn
        try:
            print(tempbtn)
            print(self.sender().text())
            a = tempbtn.index(self.sender().text())
            url = tempvid[a]
            self.secwin = secwindow(url)
            self.secwin.show()
        except Exception as e:
            print(e)

    def btnpage(self):
        try:
            text = self.sender().text()
            self.stacked_widget.setCurrentIndex(int(text) - 1)
        except Exception as e:
            print(e)

    def btnClick(self): #계약창 srch 버튼
        self.textBrowserLaw.clear()
        self.textBrowserEx.clear()
        self.labelLaw.clear()
        self.labelEx.clear()
        text = self.lineEdit.text()
        self.lineEdit.clear()
        self.lineEdit.setText(text)

        # 셀레니움 백그라운드 크롤링
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(chrome_options)  # (chrome_options)
        driver.implicitly_wait(5)
        driver.get('https://www.easylaw.go.kr/CSP/Main.laf')

        driver.find_element(By.XPATH, '//*[@id="search_input"]').send_keys(text)
        driver.find_element(By.XPATH, '//*[@id="srchForm"]/fieldset/div/button').send_keys(Keys.ENTER)

        # 예외 처리
        try:
            # 법령 정보
            self.labelLaw.setText(driver.find_element(By.XPATH, '//*[@id="result"]/ul/li[2]/h6').text)
            self.labelLaw.setStyleSheet("font-weight: bold")
            self.labelLaw.adjustSize()

            for i in range(1, 6):
                head = driver.find_element(By.XPATH, '//*[@id="result"]/ul/li[2]/ul/li[{}]/p/a'.format(i)).text
                url = driver.find_element(By.XPATH, '//*[@id="result"]/ul/li[2]/ul/li[{}]/p/a'.format(i))
                link = url.get_attribute("href")
                self.textBrowserLaw.append(str(i) + '. ' + head + ' (' + '<a href="' + link + '">자세히 보기</a>' + ')')
                if i != 5:
                    self.textBrowserLaw.append("-----------------------------------------------")

            self.btnMoreLaw.clicked.connect(self.load_urlLaw)

            # 100문 100답
            self.labelEx.setText(driver.find_element(By.XPATH, '//*[@id="result"]/ul/li[3]/h6').text)
            self.labelEx.setStyleSheet("font-weight: bold")
            self.labelEx.adjustSize()

            for i in range(1, 6):
                head = driver.find_element(By.XPATH, '//*[@id="result"]/ul/li[3]/ul/li[{}]/p/a'.format(i)).text
                url = driver.find_element(By.XPATH, '//*[@id="result"]/ul/li[3]/ul/li[{}]/p/a'.format(i))
                link = url.get_attribute("href")
                self.textBrowserEx.append(str(i) + '. ' + head + ' (' + '<a href="' + link + '">자세히 보기</a>' + ')')
                if i != 5:
                    self.textBrowserEx.append("-----------------------------------------------")

            self.btnMoreEx.clicked.connect(self.load_urlEx)

        # error 발생 시 대처 코드
        except Exception as e:
            self.textBrowserLaw.clear()
            self.textBrowserEx.clear()
            self.labelLaw.clear()
            self.labelEx.clear()
            driver.close()
            QMessageBox.critical(None, "Error", "검색된 결과가 없습니다.")

    # 더 많은 법령 정보 버튼 이벤트
    def load_urlLaw(self): #법령정보 창
        text = self.lineEdit.text()
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(
            'https://www.easylaw.go.kr/CSP/UnScRlt.laf?section=EZP_02&srchType=detail&search_put={}&outmax=20&curPage='.format(
                text))

    # 더 많은 100문 100답 버튼 이벤트
    def load_urlEx(self): #100문 100답 창
        text = self.lineEdit.text()
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(
            'https://www.easylaw.go.kr/CSP/UnScRlt.laf?section=EZP_03&srchType=detail&search_put={}&outmax=20&curPage='.format(
                text))
    def chkItemDoubleCliked(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        if self.listWidget.currentRow()%2 == 1: #----------------가 선택됐을 때 오류가 나는 것을 방지
            if self.listWidget.currentRow() == 25: #더 많을 정책보기 선택 시
                #webbrowser.open(link1)
                driver = webdriver.Chrome(chrome_options)  # (chrome_options)
                #driver.set_window_size(600, 400)
                driver.set_window_position(0, 9)
                driver.get(link1)
            else:
                try:
                    temp_srchindex = self.listWidget.currentRow()//2 #1,3,5...로 이루어진 리스트위젯의 인덱스를 0,1,2...로 변경하기 위함
                    url = (
                        'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do?pageIndex=1&frameYn=&bizId={7}&dtlOpenYn=&plcyTpOpenTy=&plcyCmprInfo=&srchWord={0}&srchPlcyTp={1}&chargerOrgCdAll=&srchRegion={2}&srchEmpStatus={3}&srchEdubg={4}&srchSpecField={5}&srchAge={6}&trgtJynEmp=&trgtJynEmp=&srchSortOrder=1&pageUnit=60'.format(
                            srchw, srchp, srchreg, srchemp, srchedu, srchspec, srcha, local_bizid[temp_srchindex]))
                    user_agent = UserAgent() #userAgent 생성
                    headers = {'user-agent': user_agent.random} #user_agent를 랜덤으로 설정해 기기 차단 우회
                    response = requests.get(url, headers=headers)

                    if response.status_code == 200:
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        title = soup.select_one('#wrap > div.container > div > div.policy-detail > h2') #정책 이름 크롤링
                        yoyak = soup.select_one('#wrap > div.container > div > div.policy-detail > p') #정책 요약 크롤링
                        # jiwon = soup.select_one('#content > div.policy-detail > div:nth-child(6) > ul > li:nth-child(3) > div.list_cont')
                        # sinc = soup.select('#content > div.policy-detail > div:nth-child(10) > ul > li:nth-child(1) > div.list_cont')
                        sinc = soup.find_all('div', {'class': 'list_cont'}) #밑의 본문 내용 크롤링을 위해 모든 list_cont 크롤링
                        temp = sinc[15].find_all(string=True) #지원 절차 크롤링
                        temp1 = sinc[18].find_all(string=True) #체출 서류 크롤링
                        temp2 = sinc[2].find_all(string=True) #지원 내용 크롤링
                        sinlink = soup.select_one(
                            '#wrap > div.container > div > div.policy-detail > div:nth-child(10) > ul > li:nth-child(3) > div.list_cont > a') # 신청 사이트 링크 크롤링
                        # seolu = soup.select('#content > div.policy-detail > div:nth-child(10) > ul > li:nth-child(4) > div.list_cont')
                    else:
                        print(response.status_code)

                    jn = [] #지원 내용
                    jj = [] #지원 자격
                    js = [] #제출 서류

                    for i in temp2: #크롤링한 지원 내용 다듬기 <br>, 공백 등 제거
                        t = i.rstrip().replace('\t', '').replace('\n', '')
                        print(t)
                        jn.append(t)

                    print('지원 절차 : ', end='')
                    for i in temp: #크롤링한 지원 절차 다듬기 <br>, 공백 등 제거
                        temp = i.rstrip().replace('\t', '').replace('\n', '')
                        print(temp)
                        jj.append(temp)

                    print('제출 서류 : ', end='')
                    for i in temp1: #크롤링한 제출 서류 내용 다듬기 <br>, 공백 등 제거
                        temp = i.rstrip().replace('\t', '').replace('\n', '')
                        print(temp)
                        js.append(temp)

                    jn1 = '\n'.join(jn) # 문장마다 \n 추가
                    jj1 = '\n'.join(jj)
                    js1 = '\n'.join(js)

                    # QMessageBox.about(self, title.get_text(), f"{yoyak.get_text()}\n\n지원 내용\n\n{jn1}\n\n지원 절차\n\n{jj1}\n\n제출 서류\n\n{js1}\n")

                    def mb(self):
                        buttonReply = QMessageBox.information(
                            self, title.get_text(), f"{yoyak.get_text()}\n\n지원 내용\n\n{jn1}\n\n지원 절차\n\n{jj1}\n\n제출 서류\n\n{js1}\n\n해당 정책 정보 및 신청 페이지로 이동하시겠습니까?",
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No) # 메세지 박스에 내용 출력

                        if buttonReply == QMessageBox.Yes:
                            if sinlink == None:
                                QMessageBox.warning(self, '신청 링크가 존재하지 않음', '신청링크가 존재하지 않아 정보 사이트로 이동합니다.')
                                driver = webdriver.Chrome(chrome_options)  # (chrome_options)
                                # driver.set_window_size(600, 1000)
                                driver.set_window_position(0, 9)
                                driver.get(url)  # webrowser를 이용해 사이트 실행
                            else:
                                # driver = webdriver.Chrome()
                                # driver.implicitly_wait(5)
                                # driver.get(str(sinlink.get_text()))
                                # webbrowser.open(str(sinlink.get_text().strip()))
                                # webbrowser.open(url, new=1) #webrowser를 이용해 사이트 실행
                                driver = webdriver.Chrome(chrome_options)  # (chrome_options)
                                # driver.set_window_size(600, 400)
                                driver.set_window_position(0, 9)
                                driver.get(str(sinlink.get_text().strip()))
                        else:
                            pass

                    mb(self)# 메세지 박스에 내용 출력
                except Exception as e:
                    print(e)

    def BtnsrchFunc(self):

        global link1
        global local_bizid

        try:

            self.listWidget.clear() # 리스트위젯 초기화
            srchw = self.lineEdit_srch.text().strip().rstrip() # 쿼리 설정을 위한 변수
            srchage = self.lineEdit_age.text().strip().rstrip()
            srchplcy = self.comboBox_plcy.currentText()
            srchreg = self.comboBox_reg.currentText()
            srchemp = self.comboBox_emp.currentText()
            srchedu = self.comboBox_edu.currentText()
            srchspec = self.comboBox_spec.currentText()

            if srchplcy == '일자리분야': # 사용자가 입력한 정보에 맞워 쿼리 설정
                srchplcy = '023010'
            elif srchplcy == '주거분야':
                srchplcy = '023020'
            elif srchplcy == '교육분야':
                srchplcy = '023030'
            elif srchplcy == '복지.문화분야':
                srchplcy = '023040'
            elif srchplcy == '참여.권리분야':
                srchplcy = '023050'
            else:
                srchplcy = ''

            if srchreg == '서울':
                srchreg = '003002001'
            elif srchreg == '부산':
                srchreg = '003002002'
            elif srchreg == '대구':
                srchreg = '003002003'
            elif srchreg == '인천':
                srchreg = '003002004'
            elif srchreg == '광주':
                srchreg = '003002005'
            elif srchreg == '대전':
                srchreg = '003002006'
            elif srchreg == '울산':
                srchreg = '003002007'
            elif srchreg == '경기':
                srchreg = '003002008'
            elif srchreg == '강원':
                srchreg = '003002009'
            elif srchreg == '충북':
                srchreg = '003002010'
            elif srchreg == '충남':
                srchreg = '003002011'
            elif srchreg == '전북':
                srchreg = '003002012'
            elif srchreg == '경북':
                srchreg = '003002013'
            elif srchreg == '경남':
                srchreg = '003002014'
            elif srchreg == '제주':
                srchreg = '003002015'
            elif srchreg == '세종':
                srchreg = '003002016'
            elif srchreg == "중앙부처":
                srchreg = '003001'
            else:
                srchreg = ''

            if srchemp == '재직자':
                srchemp = '006001'
            elif srchemp == '자영업자':
                srchemp = '006002'
            elif srchemp == '미취업자':
                srchemp = '006003'
            elif srchemp == '프리랜서':
                srchemp = '006006'
            elif srchemp == '일용근로자':
                srchemp = '006007'
            elif srchemp == '(예비)창업자':
                srchemp = '006008'
            elif srchemp == '단기근로자':
                srchemp = '006009'
            elif srchemp == '영농종사자':
                srchemp = '006010'
            elif srchemp == '제한없음':
                srchemp = '006005'
            else:
                srchemp = ''

            if srchedu == '고졸 미만':
                srchedu = '012001'
            elif srchedu == '고교 재학':
                srchedu = '012002'
            elif srchedu == '고졸 예정':
                srchedu = '012003'
            elif srchedu == '고교 졸업':
                srchedu = '012004'
            elif srchedu == '대학 재학':
                srchedu = '012005'
            elif srchedu == '대졸 예정':
                srchedu = '012006'
            elif srchedu == '대학 졸업':
                srchedu = '012007'
            elif srchedu == '석박사':
                srchedu = '012008'
            elif srchedu == '제한없음':
                srchedu = '012010'
            else:
                srchedu = ''

            if srchspec == '중소기업':
                srchspec = '007001'
            elif srchspec == '여성':
                srchspec = '007002'
            elif srchspec == '저소득층':
                srchspec = '007003'
            elif srchspec == '장애인':
                srchspec = '007004'
            elif srchspec == '농업인':
                srchspec = '007005'
            elif srchspec == '군인':
                srchspec = '007006'
            elif srchspec == '지역인제':
                srchspec = '007007'
            elif srchspec == '제한없음':
                srchspec = '007009'
            else:
                srchspec = ''

            url = (
                'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?pageIndex=1&frameYn=&bizId=&dtlOpenYn=&plcyTpOpenTy=&plcyCmprInfo=&srchWord={0}&srchPlcyTp={1}&chargerOrgCdAll=&srchRegion={2}&srchEmpStatus={3}&srchEdubg={4}&srchSpecField={5}&srchAge={6}&trgtJynEmp=&trgtJynEmp=&srchSortOrder=1&pageUnit=12'.format(
                    srchw, srchplcy, srchreg, srchemp, srchedu, srchspec, srchage))
            link1 = url

            user_agent = UserAgent() #userAgent 생성
            headers = {'user-agent': user_agent.random} #user_agent를 랜덤으로 설정해 기기 차단 우회
            response = requests.get(url, headers=headers)

            b = [] #크롤링한 내용 저장용 리스트

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.select(
                    '#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.tit-wrap > a.tit') #정책 이름 크롤링
                organ = soup.select(
                    '#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.organ-name > p:nth-child(1)') #정책 부처 크롤링
                time = soup.select(
                    '#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.organ-name > p.dday') #정책 남은 기간 크롤링
                label = soup.select(
                    '#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.badge > span.label') #정책 종료 여부 크롤링
                cate = soup.select(
                    '#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.badge > span.cate') #정책 분야 크롤링
                bizid = soup.select(
                    '#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.tit-wrap > a.tit') #정책 고유번호 크롤링

                # https: // www.youthcenter.go.kr / youngPlcyUnif / youngPlcyUnifList.do?pageIndex = 1 & frameYn = & bizId = & dtlOpenYn = & plcyTpOpenTy = & plcyCmprInfo = & srchWord = & chargerOrgCdAll = & srchAge = & trgtJynEmp = & trgtJynEmp = & srchSortOrder = 1 & pageUnit = 12
                # https: // www.youthcenter.go.kr / youngPlcyUnif / youngPlcyUnifList.do?pageIndex = 1 & frameYn = & bizId = & dtlOpenYn = & plcyTpOpenTy = & plcyCmprInfo = & srchWord = & srchPlcyTp = 023010 & chargerOrgCdAll = & srchRegion = 003001 & srchEmpStatus = 006001 & srchEdubg = 012001 & srchSpecField = 007001 & srchAge = & trgtJynEmp = & trgtJynEmp = & srchSortOrder = 1 & pageUnit = 12
                # https: // www.youthcenter.go.kr / youngPlcyUnif / youngPlcyUnifList.do?pageIndex = 1 & frameYn = & bizId = & dtlOpenYn = & plcyTpOpenTy = & plcyCmprInfo = & srchWord = & srchPlcyTp = 023010 & chargerOrgCdAll = & srchRegion = 003001 & srchEmpStatus = 006001 & srchEdubg = 012001 & srchSpecField = 007001 & srchAge = 23 & trgtJynEmp = & trgtJynEmp = & srchSortOrder = 1 & pageUnit = 12
                # https: // www.youthcenter.go.kr / youngPlcyUnif / youngPlcyUnifList.do?pageIndex = 1 & frameYn = & bizId = & dtlOpenYn = & plcyTpOpenTy = & plcyCmprInfo = & srchWord = ]& srchPlcyTp =  & chargerOrgCdAll = & srchRegion =  & srchEmpStatus =  & srchEdubg =  & srchSpecField =  & srchAge = & trgtJynEmp = & trgtJynEmp = & srchSortOrder = 1 & pageUnit = 60


                for i in range(len(title)):
                    a = []
                    a.append(title[i].get_text()) #정책 이름 크롤링
                    a.append(organ[i].get_text()) #정책 부처 크롤링
                    a.append(label[i].get_text()) #정책 종료 여부 크롤링
                    a.append(cate[i].get_text()) #정책 분야 크롤링
                    local_bizid.append(bizid[i].attrs['id'].split('_')[1])  #정책 고유번호 가공 후 저장
                    b.append(a) #2차원 리스트로 저장

                for i in b: #크롤링한 내용 출력
                    timenum = 0 #정책 남은 기간의 인덱스
                    print('-------------------------------------------------------')
                    self.listWidget.addItem('-------------------------------------------------------')
                    print('정책 이름 : ' + i[0])
                    print('기간 : ' + i[2])
                    if i[2] == '진행중': #진행중인 정책, 상시 진행인 정책, 종료된 정책 구분 구분하는 이유는 상시와 종료에는 기간이 표시되지 않아 인덱스대로 출력 시 원하는 위치에 출력되지 않음
                        print('남은 기간 : ' + time[timenum].get_text()) #크롤링한 정책의 남은 기간의 첫번째 인덱스 가져옴
                        self.listWidget.addItem('{0}\n정책 분야 : {1}\n기간 : {2}\n남은 기간 : {3}'.format(i[0], i[3], i[2], time[timenum].get_text()))
                        timenum += 1 #인덱스 += 1
                    elif i[2] != '진행중':
                        self.listWidget.addItem(
                            '{0}\n정책 분야 : {1}\n기간 : {2}'.format(i[0], i[3], i[2]))
                        timenum += 1 #인덱스 += 1

                print('-------------------------------------------------------')
                self.listWidget.addItem('-------------------------------------------------------')
                self.listWidget.addItem('>>>더 많은 정책 알아보기<<<')
            else:
                print(response.status_code)
        except Exception as e:
            print(e)

if __name__ == "__main__" :
    app = QApplication(sys.argv) #프로그램을 실행

    myWindow = WindowClass()#WindowClass의 객체 생성
    myWindow.show()#프로그램 화면을 보여주는 코드
    app.exec_()#프로그램을 작동시키는 코드