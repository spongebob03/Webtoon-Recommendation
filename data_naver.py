import re
import requests
from bs4 import BeautifulSoup

naver_url = 'https://comic.naver.com'
index = ['가','나','다','라','마','바','사','아','자','차','카','타','파','하','A','0']

def extract_base(item):
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

def get_data():
    toons = []
    for order in index:
        url = naver_url + '/webtoon/creationList?prefix={0}&view=list'.format(order)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        for item in soup.find_all('tr'):
            toon = extract_base(item)
            if not toon: continue
            toons.append(toon)
    return toons