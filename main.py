import os
import telebot
from dotenv import load_dotenv
import schedule #read more: https://schedule.readthedocs.io/en/stable/
from threading import Thread
from time import sleep
from NowRoozEvent import titleGenerator

load_dotenv()

API_KEY = os.environ['API_KEY']
CHAT_ID = -651564694 # in the future should load from DB by registering groups for this feature ^_^


bot = telebot.TeleBot(API_KEY)

def setEventTitleToGroup(chatId, prevTitle):
  eventTitle = titleGenerator(prevTitle)
  bot.set_chat_title(chatId,eventTitle)

# this script is not be always up for now
# then we set a thred on any activity in the Group
# this list helps to prevent set a new thred for the actives groups
active_group_ids = []
def setSchedule(chatId, prevTitle):
  if(chatId in active_group_ids):
    print("a relevant thread exist for: " + str(chatId))
    return
  def scheduledMethod(): 
    setEventTitleToGroup(chatId, prevTitle)
  # Thread(target=schedule.every().day.at("01:33").do(scheduledMethod)).start() 
  schedule.every().day.at("01:55").do(scheduledMethod)
  active_group_ids.append(chatId)
  print("a new thread is set for: " + str(chatId))

def schedule_checker():
  while True:
    schedule.run_pending()
    bot.send_message(CHAT_ID, "with timer per sec <3")
    sleep(1)


@bot.message_handler(commands=['salam'])
def greet(message):
  bot.reply_to(message, "Aleyke salam")
  bot.send_message(message.chat.id, "Hamegi salam")
  Thread(target=schedule_checker).start() 


@bot.message_handler(commands=['setTitle'])
def setTitle(message):
  prevTitle = message.chat.title
  chatId = message.chat.id
  print(message.chat.id)
  setEventTitleToGroup(chatId, prevTitle)

#temprory solution to listen others message
@bot.message_handler()
def checkMessages(message):
  prevTitle = message.chat.title
  chatId = message.chat.id
  print(message.chat.id)
  # setEventTitleToGroup(prevTitle, chatId)
  setSchedule(chatId, prevTitle)

# chat_id = -651564694
# bot.send_message(chat_id, "sag")

# bot.infinity_polling(interval=10, timeout=20)
bot.polling()