import sqlite3
import telebot
from telebot import types
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
# для работы selenium нужен chromedriver (в случае с Google Chrome)
# скачать нужную версию можно тут: https://chromedriver.chromium.org/downloads
# в PATH указывается путь до самого драйвера
PATH = "C:/Program Files (x86)/chromedriver.exe"
options.headless = True

# токен вашего бота
bot = telebot.TeleBot("TOKEN")


# приветствие, обработка /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item_button1 = types.KeyboardButton('Поиск по названию')
    item_button2 = types.KeyboardButton('Поиск по описанию')
    item_button3 = types.KeyboardButton('Случайный')
    markup.add(item_button1, item_button2, item_button3)
    bot.send_message(chat_id, "Что найти?", reply_markup=markup)


# основной код
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "Поиск по названию":
        with open("text.txt", "w") as f:
            f.write("название")
        chat_id = message.chat.id
        bot.send_message(chat_id, "Введите название:")
    elif message.text == "Поиск по описанию":
        with open("text.txt", "w") as f:
            f.write("описание")
        chat_id = message.chat.id
        bot.send_message(chat_id, "Введите описание:")
    elif message.text == "Случайный":
        with open("text.txt", "w") as f:
            f.write("случайный")
        chat_id = message.chat.id
        bot.send_message(chat_id, "Обрабатываю запрос...")
        db = sqlite3.connect("films_list.db")
        cur = db.cursor()
        for rand in cur.execute('SELECT * FROM Films WHERE ID IN (SELECT ID FROM Films ORDER BY RANDOM() LIMIT 1)'):
            name = rand[2]
            year = rand[3]
            description = rand[4]
            link1 = rand[5]

            driver = webdriver.Chrome(PATH, options=options)
            try:
                driver.get(link1)
                time.sleep(2)
                driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                element2 = driver.find_element(By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")
            
                result = str(element2.get_attribute('src'))
                a1 = result.split('/240.mp4')
                a2 = str(a1[0]) + "/720.mp4"
                link2 = a2
            except Exception:
                print("Ошибка")
                link2 = "Ошибка"
            driver.quit()

            q = open("text.txt", "w")
            q.write(str(name))
            q.write('\n')
            q.write(str(year))
            q.write('\n')
            q.write('\n')
            q.write(str(description))
            q.write('\n')
            q.write('\n')
            q.write(str(link1))
            q.write('\n')
            q.write('\n')
            q.write(str(link2))
            q.close()
            
            msg = open("text.txt", "r")
            msg_r = msg.read()
            chat_id = message.chat.id
            bot.send_message(chat_id, msg_r)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, "Обрабатываю запрос...")
        db = sqlite3.connect("films_list.db")
        cur = db.cursor()

        word = message.text
        r = open("text.txt", "r")
        read_r = r.read()
        if read_r == "название":
            name_list = []
            description_list = []
            year_list = []
            link1_list = []
            link2_list = []

            for name in cur.execute('SELECT NAME FROM Films WHERE NAME LIKE ?', ('%'+word+'%',)):
                name_list.append(name[0])

            for description in cur.execute('SELECT DESCRIPTION FROM Films WHERE NAME LIKE ?', ('%'+word+'%',)):
                description_list.append(description[0])

            for year in cur.execute('SELECT YEAR FROM Films WHERE NAME LIKE ?', ('%'+word+'%',)):
                year_list.append(year[0])

            for Link1 in cur.execute('SELECT LINK_STR FROM Films WHERE NAME LIKE ?', ('%'+word+'%',)):
                link1_list.append(Link1[0])

            driver = webdriver.Chrome(PATH, options=options)
            for film in link1_list:
                try:
                    driver.get(film)
                    time.sleep(2)
                    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                    element2 = driver.find_element(By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")

                    result = str(element2.get_attribute('src'))
                    a1 = result.split('/240.mp4')
                    a2 = str(a1[0]) + "/720.mp4"
                    link2_list.append(a2)
                except Exception:
                    print("Ошибка")
                    link2_list.append("Ошибка")
            driver.quit()

            for i in range(len(name_list)):
                with open("text.txt", "w") as q:
                    q.write(str(name_list[i]))
                    q.write('\n')
                    q.write(str(year_list[i]))
                    q.write('\n')
                    q.write('\n')
                    q.write(str(description_list[i]))
                    q.write('\n')
                    q.write('\n')
                    q.write(str(link1_list[i]))
                    q.write('\n')
                    q.write('\n')
                    q.write(str(link2_list[i]))

                msg = open("text.txt", "r")
                msg_r = msg.read()
                chat_id = message.chat.id
                bot.send_message(chat_id, msg_r)
                time.sleep(1)

        elif read_r == "описание":
            z = open('text.txt', 'w')
            z.seek(0)
            z.close()
            name_list = []
            description_list = []
            year_list = []
            link1_list = []
            link2_list = []
            for name in cur.execute('SELECT NAME FROM Films WHERE DESCRIPTION LIKE ?', ('%'+word+'%',)):
                name_list.append(name[0])

            for description in cur.execute('SELECT DESCRIPTION FROM Films WHERE DESCRIPTION LIKE ?', ('%'+word+'%',)):
                description_list.append(description[0])

            for year in cur.execute('SELECT YEAR FROM Films WHERE DESCRIPTION LIKE ?', ('%'+word+'%',)):
                year_list.append(year[0])

            for Link1 in cur.execute('SELECT LINK_STR FROM Films WHERE DESCRIPTION LIKE ?', ('%'+word+'%',)):
                link1_list.append(Link1[0])

            driver = webdriver.Chrome(PATH, options=options)
            for film in link1_list:
                try:
                    driver.get(film)
                    time.sleep(2)

                    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                    element2 = driver.find_element(By.XPATH, """/html/body/div/pjsdiv/pjsdiv[1]/video""")

                    result = str(element2.get_attribute('src'))

                    a1 = result.split('/240.mp4')
                    a2 = str(a1[0]) + "/720.mp4"
                    link2_list.append(a2)
                except Exception:
                    print("Ошибка")
                    link2_list.append("Ошибка")

            i = 0
            driver.quit()             
            while i < len(name_list):
                q = open("text.txt", "w")
                q.write(str(name_list[i]))
                q.write('\n')
                q.write(str(year_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(description_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(link1_list[i]))
                q.write('\n')
                q.write('\n')
                q.write(str(link2_list[i]))
                q.close()

                msg = open("text.txt", "r")
                msg_r = msg.read()
                chat_id = message.chat.id
                bot.send_message(chat_id, msg_r)
                time.sleep(1)
                i = i + 1 
                

bot.polling()
