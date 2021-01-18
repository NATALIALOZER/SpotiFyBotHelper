from bot import bot
from db import users_db

import requests
from lxml import html
import datetime 
from telebot import types
import math
import schedule
import time
import threading


#Парсинг курса
# На некоторых сайтах стоит минимальная защита и они не отдают контент без user-agent
headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}
# чтобы избежать кэширования на любом уровне, на всякий случай добавим случайно число
r = requests.get('https://finance.i.ua/bank/115/', headers=headers)

tree = html.fromstring(r.content)
kurs=tree.xpath('/html/body/div[3]/div[3]/div/div[1]/div[2]/div[1]/div/div[1]/table/tbody/tr[1]/td[2]/span/span[1]/text()')
price_spotify=7.99
suma=math.ceil((float(kurs[0])*price_spotify)/6)
print(suma)


#Постинг на канал
# Непосредственно здесь идет отправка. Инициализируем бота с помощью токена
chat_id = '-407781791'
#chat_text = 'test'

@bot.message_handler(content_types=["text"])
# def start_message(message,chat_text):
#     bot.send_message(chat_id=chat_id, text=chat_text)

def new_notifi_text(chat_id):
	chat_text='Кидаем донаты: 4441 1144 2187 9220, ' + str(suma) + ' грн.'
	todays_date = datetime.datetime.now()
	timing = 'Day: '+str(todays_date.day)
	if timing == "Day: 18":
		bot.send_message(chat_id=chat_id, text=chat_text)
		
		
def notifications(chat_id):
    """Каждый день проверяем в 12:00 не 21 ли число"""
    schedule.every().day.at('16:05').do(new_notifi_text, chat_id)
    while True:
        schedule.run_pending()
        time.sleep(3) 
		
		
if __name__ == '__main__':
    t1 = threading.Thread(target=bot.polling)
    t2 = threading.Thread(target=notifications, args=(chat_id,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

