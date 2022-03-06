import re
import requests
from bs4 import BeautifulSoup
import csv

toons = []
naver_url = 'https://comic.naver.com'
index = ['가','나','다','라','마','바','사','아','자','차','카','타','파','하','A','0']

for order in index:
    url = naver_url + '/webtoon/creationList?prefix={0}&view=list'.format(order)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    for item in soup.find_all('tr'):
        a = item.find('a', href=True)
        if not a: continue

        titleId = int(re.findall("\d+", a['href'])[0])
        title = item.find('strong').string
        rating = float(item.find('div', class_="rating_type").find('strong').string)
        date = item.find('td', class_="date").string.strip()

        toon = {
            'id': titleId,
            'title': title,
            'rating': rating,
            'date': date,
            'link': naver_url + a['href']
        }
        toons.append(toon)


def save_file(toons):
    file = open("naver.csv", mode="w", encoding="UTF8")
    writer = csv.writer(file)
    writer.writerow(["id", "title", "rating", "date", "link"])
    for toon in toons:
        writer.writerow(list(toon.values()))
    
    return 0

save_file(toons)