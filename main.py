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
    botan.track(os.environ.get('botan_key'), message.chat.id, message, 'Start.')

@bot.message_handler(content_types=['document'])
def documents_handler(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    result = validate_file_content(downloaded_file)
    if result['status']:
        bot.reply_to(message=message, text=f'https://hastebin.com/{result["result"]}', parse_mode='HTML')
        botan.track(os.environ.get('botan_key'), message.chat.id, message, 'New paste created.')
    else:
        bot.send_message(chat_id=message.chat.id, text=f'`Error: {result["message"]}`', parse_mode='Markdown')

@bot.message_handler()
def info(message):
    bot.send_message(chat_id=message.chat.id, text='*Only files are supported.*', parse_mode='Markdown')

def validate_file_content(file_object):
    file_encoding = chardet.detect(file_object)['encoding']
    if not file_encoding:
        return {'status': 0, 'message': 'incorrect file type.'}
    paste_result = paste(paste_content=file_object.decode(file_encoding).encode('utf8'))
    if isinstance(paste_result, dict):
        return {'status': 1, 'result': paste_result['key']}
    return {'status': 0, 'message': paste_result}

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=1000)
