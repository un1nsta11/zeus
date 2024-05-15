import os
import logging
import telebot

from logging import config
from telebot import types

from core.prompts import MessageView

logging.config.fileConfig(os.path.join(os.getcwd(), 'config', 'logconf.ini'))
logging = logging.getLogger('spider')


class TRat:

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.keyboard = self.create_keyboard()
        self.prompts = MessageView()

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, "This is text message", reply_markup=self.keyboard)

        @self.bot.message_handler(commands=['help'])
        def help(message):  # noqa
            self.bot.send_message(message.chat.id, 'This is a help message.')

        @self.bot.message_handler(commands=['commands'])
        def commands(message):
            self.bot.send_message(message.chat.id, 'These are the available commands.')

    def create_keyboard(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button_1 = types.KeyboardButton('/commands')
        button_2 = types.KeyboardButton('/help')
        markup.add(button_1, button_2)
        return markup

    def run(self):
        self.bot.polling()


if __name__ == '__main__':
    bot = TRat('')
    bot.run()
