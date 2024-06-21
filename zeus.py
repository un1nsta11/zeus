#!/usr/bin/env python3
import os
import logging
import telebot
import json

from logging import config
from telebot import types

from core.utils.execmd import Cmder
from prompts.prompts import Prompt, Prompts
from core.tasksch.tsch import TaskScheduler

logging.config.fileConfig(os.path.join(os.getcwd(), 'config', 'logconf.ini'))
logging = logging.getLogger('zeus')


class LoadConf:
    def load(self):
        with open(os.path.join(os.getcwd(), 'config', 'config.json')) as f:
            data = json.load(f)
        return data


class TRatMain:

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.keyboard = self.create_keyboard()

        @self.bot.message_handler(commands=['start'])
        def start(message):
            logging.debug("Remote access component: message /start requested")
            self.bot.send_message(message.chat.id, Prompt(Prompts.START).show(), reply_markup=self.keyboard)

        @self.bot.message_handler(commands=['help'])
        def help(message):  # noqa
            logging.debug("Remote access component: message /help requested")
            self.bot.send_message(message.chat.id, Prompt(Prompts.HELP).show())

        @self.bot.message_handler(commands=['commands'])
        def commands(message):
            logging.debug("Remote access component: message /commands requested")
            self.bot.send_message(message.chat.id, Prompt(Prompts.COMMANDS).show())

        @self.bot.message_handler(commands=['ipconfig'])
        def ipconfig(message):
            logging.debug("Remote access component: message /ipconfig requested")
            self.bot.send_message(message.chat.id, os.popen('ip a').read())

        @self.bot.message_handler(commands=['cmd'])
        def cmd_command(message):
            logging.debug("Remote access component: message /cmd requested")
            exec_command = '{0}'.format(message.text)
            exec_command = exec_command.split(' ')[1]
            result = Cmder(command=exec_command, workdir="/", uptime=0.1).exec_cmd(verbose=True)
            self.bot.send_message(message.chat.id, f'Result code: {result[0]} \n Output: {result[1]}')

    @staticmethod
    def create_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button_1 = types.KeyboardButton('/commands')
        button_2 = types.KeyboardButton('/help')
        markup.add(button_1, button_2)
        return markup

    def run(self):
        logging.info("Starting remote access component")
        self.bot.polling()


if __name__ == '__main__':
    # cron = TaskScheduler()
    # cron.run()
    bot = TRatMain(token=LoadConf().load()['token'])
    bot.run()
