import re
import csv
import requests
from bs4 import BeautifulSoup

naver_url = 'https://comic.naver.com'
index = ['가','나','다','라','마','바','사','아','자','차','카','타','파','하','A','1']

#region [Outline Data]
def extract_outline(item):
    a = item.find('a', href=True)
    if not a: return

    titleId = int(re.findall("\d+", a['href'])[0])
    title = item.find('strong').string
    end = True if "(완결)" in item.find('td', class_="subject").get_text() else False
    rating = float(item.find('div', class_="rating_type").find('strong').string)
    date = item.find('td', class_="date").string.strip()

    return {
        'id': titleId,
        'title': title,
        'rating': rating,
        'completed': end,
        'date': date,
        'link': naver_url + a['href']
    }

def get_outline():
    toons = []
    for order in index:
        url = naver_url + '/webtoon/creationList?prefix={0}&view=list'.format(order)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        for item in soup.find_all('tr'):
            toon = extract_outline(item)
            if not toon: continue
            toons.append(toon)
    return toons
#endregion

#region [Detail Data]
def extract_detail(id, url):
    html = requests.get(url)
    html.close()
    soup = BeautifulSoup(html.text, 'html.parser')
    detail = soup.find('div', class_="detail")
    # likes = detail.find('em', class_="u_cnt").string
    age = detail.find('span', class_="age")
    banner = soup.find("tr", class_="band_banner")
    free = True if banner and 'https://play.google.com/' in banner.find("a")["href"] else False
    
    return {
        'id': id,
        'title': detail.find('span', class_="title").string,
        'author': detail.find('span', class_="wrt_nm").string.strip(),
        'genre': detail.find('span', class_="genre").string,
        'description': detail.find('p').get_text(),
        'age': age.string if age else None,
        'free': free
    }

def get_detail(simple_file):
    f = open(simple_file, 'r')
    toons = csv.DictReader(f)
    toon_info = []
    for toon in toons:
        detail = extract_detail(toon['id'], toon['link'])
        toon_info.append(detail)
    f.close()
    return toon_info
#endregion