from bs4 import BeautifulSoup
import requests
import random
import sqlite3


# подключаем базу данных
db = sqlite3.connect("films_list.db")
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Films (ID INTEGER PRIMARY KEY, RESOURCE TEXT,
    NAME TEXT, YEAR TEXT, DESCRIPTION TEXT, LINK_STR TEXT)""")
db.commit()

# здесь нужно ввести актуальные ссылки и названия на ресурсы
resource = "lord_films"
url = "http://aj.lordfilms-s.tv/filmy/"

# список user_agent'ов
user_agent_list = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/83.0.4103.97 Safari/537.36",
]
user_agent = random.choice(user_agent_list)
headers = {'User-Agent': user_agent}

# перебор всех страниц с фильмами на сайте
# вместо 2076 нужно поставить актуальное число страниц
page_number = 1
while page_number < 2076:
    page = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")
    name_list = []
    year_list = []
    link1_list = []
    description_list = []

    for name in page.find_all("div", class_="th-title"):
        name_text = name.text
        print(name_text)
        name_list.append(name_text)

    for year in page.find_all("div", class_="th-year"):
        year_text = year.text
        year_list.append(year_text)

    for film in page.find_all("div", class_="th-item"):
        Link_STR = film.find("a", class_="th-in with-mask").get('href')
        link1_list.append(Link_STR)

    for link0 in link1_list:
        page2 = BeautifulSoup(requests.get(link0, headers=headers).text, "lxml")
        description = page2.find("div", class_="fdesc clearfix slice-this").text

        b_split_list = description.split("						")
        b1 = b_split_list[-1]
        description_list.append(b1)

    for i in range(len(description_list)):
        name1 = name_list[i]
        year1 = year_list[i]
        description1 = description_list[i]
        link2 = link1_list[i]

        # сохраняем данные в БД
        cur.execute("""INSERT INTO Films (RESOURCE, NAME, YEAR, DESCRIPTION, LINK_STR) VALUES (?, ?, ?, ?, ?);""",
                    (resource, name1, year1, description1, link2))
        db.commit()

    page_number += 1
    url = "http://aj.lordfilms-s.tv/filmy/page/" + str(page_number) + "/"
