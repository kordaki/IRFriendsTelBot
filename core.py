import os
import telebot
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ['API_KEY']
LOG_CHANNEL_ID = os.environ['LOG_CHANNEL_ID']
ADMIN_LIST = os.environ['ADMIN_LIST'].split(',')
bot = telebot.TeleBot(API_KEY)


def setLog(message):
  if message.chat.type != 'private':
    return
  bot.forward_message(LOG_CHANNEL_ID, message.chat.id, message.id)
  bot.send_message(LOG_CHANNEL_ID, "👆 user id: " + str(message.from_user.id))


userDic = {}
def directMessageByAdmin(message):
  if str(message.from_user.id) not in ADMIN_LIST:
    bot.reply_to(message, "⛔️ You're not Admin")
    return
  splitedMessage = message.text.split(' ')
  if len(splitedMessage) == 1:
    bot.reply_to(message, "⚠️ add user id after the command")
    return
  if len(userDic) > 0:
    firstAdminId = next(iter(userDic))
    bot.send_message(message.chat.id, f"✏️ Admin {firstAdminId} is writing message to {userDic[firstAdminId]}")
  targetUserId = splitedMessage[1]
  userDic[message.chat.id] = targetUserId
  msg = bot.reply_to(message, "Salam admin 👋🏼 \nWrite your message :)")
  bot.register_next_step_handler(msg, sendAdminMessageToUser)

def sendAdminMessageToUser(message):
  try:
    chatId = message.chat.id
    targetUserId = userDic[chatId]
    content = message.text
    bot.send_message(targetUserId, content)
    bot.reply_to(message, "✅ Sent!")
    bot.send_message(LOG_CHANNEL_ID, f"✉️ Message from Admin: `{chatId}` to `{targetUserId}`: \n{content}")
    userDic.pop(chatId)
  except Exception as e:
    print(message)
    bot.reply_to(message, 'oooops, try again')