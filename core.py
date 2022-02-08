import os
import telebot
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)