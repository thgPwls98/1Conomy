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

import csv
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context

# srchp
# 일자리 : 023010
# 주거 :  023020
# 교육 : 023030
# 복지 : 023040
# 참여 : 023050
# srchreg
# 중앙부처 : 003001
# 서울 : 003002001
# 부산 : 003002002
# 대구 : 003002003
# 인천 : 003002004
# 광주 : 003002005
# 대전 : 003002006
# 울산 : 003002007
# 경기 : 003002008
# 강원 : 003002009
# 충북 : 003002010
# 충남 : 003002011
# 전북 : 003002012
# 전남 : 003002013
# 경북 : 003002014
# 경남 : 003002015
# 제주 : 003002016
# 세종 : 003002017
#
# srchemp
# 전체 선택 :
# 재직자 : 006001
# 자영업자 : 006002
# 미취업자 : 006003
# 프리랜서 : 006006
# 일용근로자 : 006007
# (예비)창업자 : 006008
# 단기근로자 : 006009
# 영농종사자 : 006010
# 제한없음 : 006005
#
# srchedu
# 전체 선택 :
# 고졸 미만 : 012001
# 고교 재학 : 012002
# 고졸 예정 : 012003
# 고교 졸업 : 012004
# 대학 재학 : 012005
# 대졸 예정 : 012006
# 대학 졸업 : 012007
# 석박사 : 012008
# 제한없음 : 012010
#
# srchspec
# 전체 선택
# 중소기업 : 007001
# 여성 : 007002
# 저소득층 : 007003
# 장애인 : 007004
# 농업인 : 007005
# 군인 : 007006
# 지역인재 : 007007
# 제한없음 : 007009



print('단어를 입력하시오 : ', end = '')
word = input()

print('정책 분야를 입력하시오 : ', end = '')
p = input()
if p == '일자리':
    p = '023010'
elif p == '주거':
    p = '023020'
elif p == '교육':
    p = '023030'
elif p == '복지':
    p = '023040'
elif p == '참여':
    p = '023050'

print('지역을 입력하시오 : ', end = '')
reg = input()
if reg == '서울':
    reg = '003002001'
elif reg == '부산':
    reg = '003002002'
elif reg == '대구':
    reg = '003002003'
elif reg == '인천':
    reg = '003002004'
elif reg == '광주':
    reg = '003002005'
elif reg == '대전':
    reg = '003002006'
elif reg == '울산':
    reg = '003002007'
elif reg == '경기':
    reg = '003002008'
elif reg == '강원':
    reg = '003002009'
elif reg == '충북':
    reg = '003002010'
elif reg == '충남':
    reg = '003002011'
elif reg == '전북':
    reg = '003002012'
elif reg == '경북':
    reg = '003002013'
elif reg == '경남':
    reg = '003002014'
elif reg == '제주':
    reg = '003002015'
elif reg == '세종':
    reg = '003002016'
elif reg == "중앙부처":
    reg = '003001'

print('직업 상태를 입력하시오 : ', end = '')
state = input()
if state == '재직자':
    state = '006001'
elif state == '자영업자':
    state = '006002'
elif state == '미취업자':
    state = '006003'
elif state == '프리랜서':
    state = '006006'
elif state == '일용근로자':
    state = '006007'
elif state == '(예비)창업자':
    state = '006008'
elif state == '단기근로자':
    state = '006009'
elif state == '영농종사자':
    state = '006010'
elif state == '제한없음':
    state = '006005'


print('교육 상태를 입력하시오 : ', end = '')
edu = input()
if edu == '고졸 미만':
    edu = '012001'
elif edu == '고교 재학':
    edu = '012002'
elif edu == '고졸 예정':
    edu = '012003'
elif edu == '고교 졸업':
    edu = '012004'
elif edu == '대학 재학':
    edu = '012005'
elif edu == '대졸 예정':
    edu = '012006'
elif edu == '대학 졸업':
    edu = '012007'
elif edu == '석박사':
    edu = '012008'
elif edu == '제한없음':
    edu = '012010'


print('사회적 위치를 입력하시오 : ', end = '')
spec = input()
if spec == '중소기업':
    spec = '007001'
elif spec == '여성':
    spec = '007002'
elif spec == '저소득층':
    spec = '007003'
elif spec == '장애인':
    spec = '007004'
elif spec == '농업인':
    spec = '007005'
elif spec == '군인':
    spec = '007006'
elif spec == '지역인제':
    spec = '007007'
elif spec == '제한없음':
    spec = '007009'

print('나이를 입력하시오 : ', end = '')
age = input()

biz = ''

url = ('https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?pageIndex=1&frameYn=&bizId=&dtlOpenYn=&plcyTpOpenTy=&plcyCmprInfo=&srchWord={0}&srchPlcyTp={1}&chargerOrgCdAll=&srchRegion={2}&srchEmpStatus={3}&srchEdubg={4}&srchSpecField={5}&srchAge={6}&trgtJynEmp=&trgtJynEmp=&srchSortOrder=1&pageUnit=12'.format(word, p, reg, state, edu, spec, age))

user_agent = UserAgent()
headers = {'user-agent': user_agent.random}

response = requests.get(url, headers=headers)

b = []

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.tit-wrap > a.tit')
    organ = soup.select('#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.organ-name > p:nth-child(1)')
    time = soup.select('#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.organ-name > p.dday')
    label = soup.select('#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.badge > span.label')
    cate = soup.select('#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.badge > span.cate')
    bizid = soup.select('#srchFrm > div.sch-result-wrap > div.result-list-wrap > ul > li > div.result-card-box > div.tit-wrap > a.tit')

    #https: // www.youthcenter.go.kr / youngPlcyUnif / youngPlcyUnifList.do?pageIndex = 1 & frameYn = & bizId = & dtlOpenYn = & plcyTpOpenTy = & plcyCmprInfo = & srchWord = & chargerOrgCdAll = & srchAge = & trgtJynEmp = & trgtJynEmp = & srchSortOrder = 1 & pageUnit = 12
    #https: // www.youthcenter.go.kr / youngPlcyUnif / youngPlcyUnifList.do?pageIndex = 1 & frameYn = & bizId = & dtlOpenYn = & plcyTpOpenTy = & plcyCmprInfo = & srchWord = & srchPlcyTp = 023010 & chargerOrgCdAll = & srchRegion = 003001 & srchEmpStatus = 006001 & srchEdubg = 012001 & srchSpecField = 007001 & srchAge = & trgtJynEmp = & trgtJynEmp = & srchSortOrder = 1 & pageUnit = 12
    #https: // www.youthcenter.go.kr / youngPlcyUnif / youngPlcyUnifList.do?pageIndex = 1 & frameYn = & bizId = & dtlOpenYn = & plcyTpOpenTy = & plcyCmprInfo = & srchWord = & srchPlcyTp = 023010 & chargerOrgCdAll = & srchRegion = 003001 & srchEmpStatus = 006001 & srchEdubg = 012001 & srchSpecField = 007001 & srchAge = 23 & trgtJynEmp = & trgtJynEmp = & srchSortOrder = 1 & pageUnit = 12
    #https: // www.youthcenter.go.kr / youngPlcyUnif / youngPlcyUnifList.do?pageIndex = 1 & frameYn = & bizId = & dtlOpenYn = & plcyTpOpenTy = & plcyCmprInfo = & srchWord = ]& srchPlcyTp =  & chargerOrgCdAll = & srchRegion =  & srchEmpStatus =  & srchEdubg =  & srchSpecField =  & srchAge = & trgtJynEmp = & trgtJynEmp = & srchSortOrder = 1 & pageUnit = 60
    for i in range(len(title)):
        a = []
        a.append(title[i].get_text())
        a.append(organ[i].get_text())
        a.append(label[i].get_text())
        a.append(cate[i].get_text())
        a.append(bizid[i].attrs['id'].split('_')[1])
        b.append(a)

    for i in b:
        timenum = 0
        print('-------------------------------------------------------')
        print('정책 이름 : ' + i[0])
        print('기간 : ' + i[2])
        if i[2] != '상시':
            print('남은 기간 : ' + time[timenum].get_text())
            timenum += 1
        elif i[2] != '신청 마감':
            timenum += 1
    print('-------------------------------------------------------')

else:
    print(response.status_code)

print('알고 싶은 정책을 입력하시오 : ', end = '')
urselc = input()

for a in b:
    if a[0] == urselc:
        biz = a[4]

url = ('https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do?pageIndex=1&frameYn=&bizId={7}&dtlOpenYn=&plcyTpOpenTy=&plcyCmprInfo=&srchWord={0}&srchPlcyTp={1}&chargerOrgCdAll=&srchRegion={2}&srchEmpStatus={3}&srchEdubg={4}&srchSpecField={5}&srchAge={6}&trgtJynEmp=&trgtJynEmp=&srchSortOrder=1&pageUnit=60'.format(word, p, reg, state, edu, spec, age, biz))
response = requests.get(url, headers=headers)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    yoyak = soup.select_one('#content > div.policy-detail > p')
    #jiwon = soup.select_one('#content > div.policy-detail > div:nth-child(6) > ul > li:nth-child(3) > div.list_cont')
    #sinc = soup.select('#content > div.policy-detail > div:nth-child(10) > ul > li:nth-child(1) > div.list_cont')
    sinc = soup.find_all('div', {'class': 'list_cont'})
    temp = sinc[15].find_all(string=True)
    temp1 = sinc[18].find_all(string=True)
    sinlink = soup.select_one('#content > div.policy-detail > div:nth-child(10) > ul > li:nth-child(3) > div.list_cont > a')
    #seolu = soup.select('#content > div.policy-detail > div:nth-child(10) > ul > li:nth-child(4) > div.list_cont')
else:
   print(response.status_code)

print('-------------------------------------------------------')
print(yoyak.get_text())

print('지원 절차 : ', end = '')
for i in temp:
    print(i.rstrip().replace('\t', '').replace('\n', ''))

print('제출 서류 : ', end = '')
for i in temp1:
    print(i.rstrip().replace('\t', '').replace('\n', ''))

driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.get(str(sinlink.get_text()))

#content > div.policy-detail > div:nth-child(6) > ul > li:nth-child(3) > div.list_cont > br

while(True):
    print('종료하시곘습니까?', end = '')
    if input() == '네':
        break