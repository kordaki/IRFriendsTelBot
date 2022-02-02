import os
from datetime import date
import re
import telebot

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

def daysCounter():
  today = date.today()
  nowRooz = date(2022, 3, 21)
  delta = nowRooz - today
  return delta.days

def addDaysToTitle(title, daysToNowRooz):
  selectedNumber = re.findall(r'\[(\d+)\]', title)
  newTitle = ""
  if len(selectedNumber) > 0 :
    newTitle = title.replace(selectedNumber[0], daysToNowRooz)
  else:
    newTitle = title + " ["+daysToNowRooz+"]"
  return newTitle

def titleGenerator(prevTitle):
  daysToNowRooz = daysCounter()
  if daysToNowRooz < 1:
    return
  newTitle = addDaysToTitle(prevTitle , str(daysToNowRooz))
  print(newTitle)
  return newTitle

@bot.message_handler(commands=['salam'])
def greet(message):
  bot.reply_to(message, "Aleyke salam")
  bot.send_message(message.chat.id, "Hamegi salam")

@bot.message_handler(commands=['setTitle'])
def greet(message):
  prevTitle = message.chat.title
  nowRoozTitle = titleGenerator(prevTitle)
  bot.set_chat_title(message.chat.id,nowRoozTitle)

# chat_id = -651564694
# bot.send_message(chat_id, "sag")



# bot.infinity_polling(interval=10, timeout=20)
bot.polling()