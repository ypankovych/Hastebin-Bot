import os
import botan
import telebot
from hastebin import paste

bot = telebot.TeleBot(os.environ.get('token'))

@bot.message_handler(commands=['start'])
def start(message):
    with open('hello_message.txt') as hello_msg:
        bot.send_message(chat_id=message.chat.id, text=hello_msg.read(), parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def documents_handler(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    paste_link = paste(paste_content=downloaded_file)
    if paste_link:
        bot.send_message(chat_id=message.chat.id, text=f'https://hastebin.com/{paste_link}', parse_mode='HTML')
        botan.track(os.environ.get('botan_key'), message.chat.id, message, 'New paste created.')
    else:
        bot.send_message(chat_id=message.chat.id, text='`Error: Invalid file format`', parse_mode='Markdown')

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)