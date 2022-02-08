import schedule #read more: https://schedule.readthedocs.io/en/stable/
from threading import Thread
from time import sleep
from nowRoozEvent import setEventTitleToGroup
from core import bot, setLog, directMessageByAdmin

CHAT_ID = -651564694 # in the future it should load from DB by registering groups for this feature ^_^


# this script is not be always up for now
# then we set a thread on any activity in the Group
# this list helps to prevent set a new thread for the actives groups
active_group_ids = []
def setSchedule(chatId, prevTitle):
  if(chatId in active_group_ids):
    print(f"a relevant thread exist for: {chatId}")
    return
  def scheduledMethod(): 
    print(f"inside of the schedule method is running... {chatId} prevTitle: {prevTitle}")
    setEventTitleToGroup(chatId, prevTitle)
  schedule.every().day.at("09:00").do(scheduledMethod)
  # schedule.every().minute.at(":17").do(scheduledMethod)
  active_group_ids.append(chatId)
  print(f"a new thread is set for: {chatId}")

def schedule_checker():
  while True:
    schedule.run_pending()
    sleep(1)
Thread(target=schedule_checker).start() 

@bot.message_handler(commands=['salam'])
def greet(message):
  bot.reply_to(message, "Aleyke salam")
  bot.send_message(message.chat.id, "Hamegi salam")
  

@bot.message_handler(commands=['setTitle'])
def setTitle(message):
  prevTitle = message.chat.title
  chatId = message.chat.id
  print(message.chat.id)
  setEventTitleToGroup(chatId, prevTitle)

@bot.message_handler(commands=['direct'])
def handleDirectMessage(message):
  directMessageByAdmin(message)

@bot.message_handler()
def checkMessages(message):
  prevTitle = message.chat.title
  chatId = message.chat.id
  print(message.chat.id)
  setLog(message)
  setSchedule(chatId, prevTitle)


# chat_id = -651564694
# bot.send_message(chat_id, "sag")

bot.polling()