import os
import botan
import chardet
import telebot
from hastebin import paste

bot = telebot.TeleBot(os.environ.get('token'))

@bot.message_handler(commands=['start'])
def start(message):
    with open('hello_message.txt') as hello_msg:
        bot.send_message(chat_id=message.chat.id, text=hello_msg.read(), parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def documents_handler(message):
    if message.document.mime_type.split('/')[0] == 'text':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        paste_link = paste(paste_content=downloaded_file.decode(chardet.detect(downloaded_file)['encoding']).encode('utf8'))
        if isinstance(paste_link, dict):
            bot.reply_to(message=message, text=f'https://hastebin.com/{paste_link["key"]}', parse_mode='HTML')
            botan.track(os.environ.get('botan_key'), message.chat.id, message, 'New paste created.')
        else:
            bot.send_message(chat_id=message.chat.id, text=f'`Error: {paste_link}`', parse_mode='Markdown')
    else:
        bot.send_message(chat_id=message.chat.id, text='`Error: incorrect file type.`', parse_mode='Markdown')

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
