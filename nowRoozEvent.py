import os
from datetime import date
import re
from persiantools import digits
from core import bot
from dotenv import load_dotenv

load_dotenv()

EVENT = os.environ['EVENT']
DATE = os.environ['DATE'] # Iso format 2022-03-20
CONCAT_STR = os.environ['CONCAT_STR']

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

def setEventTitleToGroup(chatId, prevTitle):
  eventTitle = titleGenerator(prevTitle)
  bot.set_chat_title(chatId,eventTitle)