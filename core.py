import os
import telebot
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ['API_KEY']
LOG_CHANNEL_ID = os.environ['LOG_CHANNEL_ID']

bot = telebot.TeleBot(API_KEY)

def setLog(message):
  if message.chat.type != 'private':
    return
  bot.forward_message(LOG_CHANNEL_ID, message.chat.id, message.id)
  bot.send_message(LOG_CHANNEL_ID, "👆 user id:" + str(message.from_user.id))
  print(message)