from dotenv import load_dotenv
import telebot
import os
from PIL import Image

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hi {message.chat.first_name}, send me a photo with german words!')
    print(message.chat)
    print(f'Hi {message.chat.first_name}, send me a photo with german words!')

@bot.message_handler(content_types=['photo'])
def main(message):
    bot.reply_to(message, "Good photo")


bot.polling(none_stop=True)