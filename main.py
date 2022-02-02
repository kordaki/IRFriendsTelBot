import os
from datetime import date
import re
import telebot
from dotenv import load_dotenv
from persiantools import digits


load_dotenv()

EVENT = os.environ['EVENT']
DATE = os.environ['DATE'] # Iso format 2022-04-19
CONCAT_STR = os.environ['CONCAT_STR']
API_KEY = os.environ['API_KEY']

bot = telebot.TeleBot(API_KEY)

def daysCounter():
  today = date.today()
  date_of_event = date.fromisoformat(DATE)
  delta = date_of_event - today
  return delta.days

def addDaysToTitle(title, daysToEvent):
  strDaysToEvent = digits.en_to_fa(str(daysToEvent))
  selectedTitlePart = re.findall(r'\«(\d+\s.*?)\»', title)
  newTitlePart = strDaysToEvent + CONCAT_STR + EVENT
  if len(selectedTitlePart) > 0 :
    newTitle = title.replace(selectedTitlePart[0], newTitlePart)
  else:
    # FIX: RTL issue.
    # Maybe adding a farsi character in the begiging solve the issue!
    newTitle = title + "«" + newTitlePart + "»"
  return newTitle

def titleGenerator(prevTitle):
  daysToEvent = daysCounter()
  if daysToEvent < 1:
    return
  newTitle = addDaysToTitle(prevTitle , daysToEvent)
  print(newTitle)
  return newTitle

@bot.message_handler(commands=['salam'])
def greet(message):
  bot.reply_to(message, "Aleyke salam")
  bot.send_message(message.chat.id, "Hamegi salam")

@bot.message_handler(commands=['setTitle'])
def setTitle(message):
  prevTitle = message.chat.title
  eventTitle = titleGenerator(prevTitle)
  print(message.chat.id)
  bot.set_chat_title(message.chat.id,eventTitle)

#temprory solution to lissten others message
@bot.message_handler()
def checkMessages(message):
  prevTitle = message.chat.title
  eventTitle = titleGenerator(prevTitle)
  print(message.chat.id)
  bot.set_chat_title(message.chat.id,eventTitle)

# chat_id = -651564694
# bot.send_message(chat_id, "sag")



# bot.infinity_polling(interval=10, timeout=20)
bot.polling()
