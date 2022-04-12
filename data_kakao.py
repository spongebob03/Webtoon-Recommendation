import re
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from save import save_file

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 카카오웹툰 레이아웃 안 데이터는 자바스크립트인가 내부가 bs로 스크랩이 안됨
kakao_url = "https://webtoon.kakao.com/original-"

#region In Grid page
def get_links():
    links = []
    driver = webdriver.Chrome()
    extract_from_page(driver, kakao_url+"webtoon", links)
    extract_from_page(driver, kakao_url+"novel", links)
    extract_from_complete(driver, kakao_url+"webtoon?tab=complete", links)
    extract_from_complete(driver, kakao_url+"novel?tab=complete", links)

    save_file(links, "k-simple")

def extract_from_page(driver, page, links):
    driver.get(page)
    driver.implicitly_wait(10)

    elems = driver.find_elements(By.XPATH,"//a[contains(@href,'content')]")
    for elem in elems:
        link = elem.get_attribute('href')
        links.append({'id': link.split('/')[-1], 'link': link, 'completed': False})
    print(f'...finish extract ({len(elems)}) links from {page}')

def extract_from_complete(driver, page, links):
    driver.get(page)
    wait = WebDriverWait(driver,30)

    elems = []
    SCROLL_LIMIT = 45
    for i in range(SCROLL_LIMIT+1):
        # Wait for the elements to load/appear
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'content')]")))
        # Get all the elements which contains href value
        elems = driver.find_elements(By.XPATH,"//a[contains(@href,'content')]")
        # Scroll to the last element of the list links
        driver.execute_script("arguments[0].scrollIntoView(true);",elems[len(elems)-1])

    # Iterate to print the links
    for elem in elems:
        link = elem.get_attribute('href')
        links.append({'id': link.split('/')[-1], 'link': link, 'completed': True})

    print(f'...finish extract ({len(elems)}) links from {page}')
#endregion

#region in webtoon home - 1200여개 링크 중 208밖에 못 갖고 오고 있음
def get_detail(link_file):
    f = open(link_file, 'r')
    toons = csv.DictReader(f)
    toon_info = []
    for toon in toons:
        detail = extract_from_detail(toon['link'])
        if detail:
            toon_info.append(detail)
    f.close()
    return toon_info

def extract_from_detail(url):
    html = requests.get(url)
    html.close()
    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        description = soup.find("meta", {"name":"description"})['content']
        container = soup.find("div", class_="overflow-hidden cursor-pointer")
        data = []
        for word in container.find_all("p"):
            data.append(word.string)
    except:
        # print(f'CAN NOT EXTRACT FROM {url}')
        return None
    return {
        "id": int(url.split('/')[-1]),
        "title": data[0],
        "author": data[1],
        "genre": data[2],
        "views": data[3],
        "likes": data[4],
        "description": description,
        "link": url
    }
#endregion

get_links()

kakao_webtoon = get_detail('k-simple.csv')
save_file(kakao_webtoon, "k-detail")