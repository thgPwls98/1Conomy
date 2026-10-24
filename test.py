import requests
from bs4 import BeautifulSoup


url = 'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifDtl.do?pageIndex=1&frameYn=&bizId=R2023051302901&dtlOpenYn=&plcyTpOpenTy=&plcyCmprInfo=&srchWord=%EC%95%8C%EB%9C%B0%EA%B5%90%ED%86%B5%EC%B9%B4%EB%93%9C&chargerOrgCdAll=&srchAge=&trgtJynEmp=&trgtJynEmp=&srchSortOrder=1&pageUnit=12'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find_all('div', {'class' : 'list_cont'})
    for i in ul:
        print(i.find_all(string = True))
    temp = ul[15].find_all(string = True)
    temp1 = ul[18].find_all(string = True)
    for i in temp:
        print(i.rstrip().replace('\t', ''))
    for i in temp1:
        print(i.rstrip().replace('\t', '').replace('\n', ''))
else:
    print(response.status_code)

url = 'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do'

response = requests.get(url)

a = []

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    for i in range(1, 11):
        ul = soup.select_one('#srchFrm > div.ply-srh-box.explain-srh-box > div.policy-search.blue-type > div.detail_search > div > div:nth-child(3) > div.view_cont > ul > li:nth-child({}) > span'.format(i))
        print(ul.get_text())
        a.append(ul.get_text().strip('\n'))
else:
    print(response.status_code)

print(a)
#srchFrm > div.ply-srh-box.explain-srh-box > div.policy-search.blue-type > div:nth-child(3) > div.r.ply-op > ul > li:nth-child(1) > span

