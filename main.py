from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from requests import Session
from loguru import logger

import time
import os


def http_get_url(url_function, page_function=None):
    if page_function:
        url_function += f"&page={page_function}"
    try:
        response = http.get(url_function, headers={
            'upgrade-insecure-requests': "1",
            'user-agent': ua.random
        })
    except:
        return False
    if response.status_code != 200:
        return False
    return response

def exits():
    os.system("pause")
    logger.debug(f"log: {name_log}")
    exit()


name_log = f"result/result_{time.strftime('%H_%M_%S')}.txt"
if not os.path.isdir("result/"):
    os.mkdir("result/")
with open(name_log, "w", encoding="utf-8") as file:
    pass

logger.debug("Введите запрос: ")
search = input()
logger.debug("0 - ALL, 1 - EN, 2 - RU: ")
langs = int(input())
lang = ["", "en", "ru"][langs]
search_url = "https://tgpulse.com/ru/search" + f"?search={search}&order=best&lang={lang}&category="


http = Session()
ua = UserAgent()

page = 1
while True:
    search_result = http_get_url(search_url, page)

    if not search_result:
        logger.error("Не удалось получить ответ от сервера")
        exits()

    soup = BeautifulSoup(search_result.text, "lxml")
    pages = soup.find_all("div", {"class": "col-md-6"})
    info = soup.find_all("div", {"class": "p-1"})
    if len(info) == 3 and page == 1:
        logger.info(info[2].find("h1").text)

    for i in pages:
        info_url = f"https://tgpulse.com" + i.find("a")['href']

        info_results = http_get_url(info_url)

        soup = BeautifulSoup(info_results.text, "lxml")

        asset = soup.find("div", {"class": "col-7"}).find("b").text
        list_info = soup.find_all("span", {"data-plugin": "counterup"})
        link_tg = soup.find("a", {"itemprop": "url"})['href'].replace('https://', '')

        if len(list_info) != 3:
            logger.error(f"Неполная информация об {info_url}")

        with open(name_log, "a", encoding="utf-8") as file:
            file.write(f"{link_tg} {asset}")
            for i in list_info:
                file.write(f" {i.text}")
            file.write("\n")

    if not pages:
        exits()

    logger.success(f"Записал {len(pages)}")

    page += 1




