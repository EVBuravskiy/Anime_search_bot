import telebot
from bot_config import keyboard_start, keyboard_run, keyboard_genre, random_movie
from bot_token import token
from create_dict import get_dict


"""Telebot designed to search for anime from animestars.org by parsing the site"""


bot = telebot.TeleBot(token=token)
url = 'https://animestars.org/topanime.html'
title = ''
dict_of_ganres = {}


@bot.message_handler(commands=['start'])
def start_com(message):
    greetings = 'Welcome to the film search bot!!!\nWhat is your name?'
    bot.send_message(message.chat.id, greetings)
    bot.register_next_step_handler(message, reg_name)


def reg_name(message):
    global title
    title = message.text
    bot.send_message(message.chat.id, f'Nice to meet you {title}!\nTo get started, send the "/run" command\nIf you need help send "/help"\n Or click the button', reply_markup=keyboard_start())


@bot.message_handler(commands=['help'])
def help_com(message):
    help_text = """
    To restart the bot, enter the command "/start"
    To get help, enter the command "/help"
    To start the bot, enter the command "/run"
    To work comfortably with the bot, use the keyboard that appears after sending the “/run” command
    """
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['run'])
def run_com(message):
    bot.send_message(message.chat.id, "Lets go!;)", reply_markup=keyboard_run())


@bot.message_handler(content_types=['text'])
def genre_reply(message):
    if message.text == 'Anime genres (animestars.org)':
        bot.send_message(message.chat.id, 'Choose one of the genres: ', reply_markup=keyboard_genre())

    if message.text == 'Random from Chinese anime (animestars.org)':
        url = 'https://animestars.org/aniserials/chinese/'
        random_search = random_movie(url)
        if random_search != None:
            title, link = random_search
            bot.send_message(message.chat.id, f'A random anime named {title} has been selected for you\nYou can watch it at the link: {link}')
        else:
            bot.send_message(message.chat.id, 'Sorry, the server is not available. Try again')
    if message.text == 'Random anime from top 100 (animestars.org)':
        url = 'https://animestars.org/topanime.html'
        random_search = random_movie(url)
        if random_search != None:
            title, link = random_search
            bot.send_message(message.chat.id, f'A random anime named {title} has been selected for you\nYou can watch it at the link: {link}')
        else:
            bot.send_message(message.chat.id, 'Sorry, the server is not available. Try again')


@bot.callback_query_handler(func=lambda call: True)
def genre_reply_button(call):
    key = call.data
    bot.send_message(call.message.chat.id, f"You chose {call.data}")
    dict_of_ganres = get_dict()
    genre_urls = f"https://animestars.org{dict_of_ganres[key]}"
    title, link = random_movie(genre_urls)
    bot.send_message(call.message.chat.id, f'A random anime from genre {call.data} named {title} has been selected for you\nYou can watch it at the link: {link}')


bot.polling()

