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

    def __init__(self):
        self.config = None

    def config(self):
        with open(os.path.join(os.getcwd(), 'config', 'config.json')) as f:
            self.config = json.load(f)
        return self.config


class TRatMain:

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.keyboard = self.create_keyboard()

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, Prompt(Prompts.START).show(), reply_markup=self.keyboard)

        @self.bot.message_handler(commands=['help'])
        def help(message):  # noqa
            self.bot.send_message(message.chat.id, Prompt(Prompts.HELP).show())

        @self.bot.message_handler(commands=['commands'])
        def commands(message):
            self.bot.send_message(message.chat.id, Prompt(Prompts.COMMANDS).show())

        @self.bot.message_handler(commands=['ipconfig'])
        def ipconfig(message):
            self.bot.send_message(message.chat.id, os.popen('ip a').read())

        @self.bot.message_handler(commands=['cmd'])
        def cmd_command(message):
            exec_command = '{0}'.format(message.text)
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
        self.bot.polling()


if __name__ == '__main__':
    cron = TaskScheduler()
    cron.run()

    bot = TRatMain(token=LoadConf().config()['token'])
    bot.run()
