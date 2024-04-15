import telebot.types
import requests
from bs4 import BeautifulSoup as bs
import random

dict_of_movies = {}
list_of_title = []

def keyboard_start():
    keyboard_markup = telebot.types.ReplyKeyboardMarkup()
    btn_run = telebot.types.KeyboardButton('/run')
    btn_help = telebot.types.KeyboardButton('/help')
    keyboard_markup.row(btn_run, btn_help)
    return keyboard_markup


def keyboard_run():
    keyboard_markup = telebot.types.ReplyKeyboardMarkup()
    btn_genre = telebot.types.KeyboardButton('Anime genres (animestars.org)')
    btn_random_popular_movie = telebot.types.KeyboardButton('Random from Chinese anime (animestars.org)')
    btn_random_top100 = telebot.types.KeyboardButton('Random anime from top 100 (animestars.org)')
    keyboard_markup.row(btn_genre)
    keyboard_markup.row(btn_random_popular_movie)
    keyboard_markup.row(btn_random_top100)
    return keyboard_markup


def keyboard_genre():
    keyboard_genre_reply = telebot.types.InlineKeyboardMarkup()
    key_action = telebot.types.InlineKeyboardButton(text="Action movie", callback_data='Экшен')
    key_martial = telebot.types.InlineKeyboardButton(text="Martial arts", callback_data='Боевые искусства')
    key_vampires = telebot.types.InlineKeyboardButton(text="Vampires", callback_data='Вампиры')
    key_war = telebot.types.InlineKeyboardButton(text="War", callback_data='Война')
    key_garem = telebot.types.InlineKeyboardButton(text="Garem", callback_data='Гарем')
    key_detective = telebot.types.InlineKeyboardButton(text="Detective", callback_data='Детектив')
    key_drama = telebot.types.InlineKeyboardButton(text="Drama", callback_data='Драма')
    key_game = telebot.types.InlineKeyboardButton(text="Game", callback_data="Игра")
    key_history = telebot.types.InlineKeyboardButton(text='History', callback_data='История')
    key_comedy = telebot.types.InlineKeyboardButton(text='Comedy', callback_data='Комедия')
    key_mexa = telebot.types.InlineKeyboardButton(text='Mech', callback_data='Меха')
    keyboard_genre_reply.add(key_action, key_martial, key_war, key_vampires, key_detective, key_game, key_garem,
                             key_drama, key_history, key_comedy, key_mexa)
    return keyboard_genre_reply


def random_movie(url):
    """Function of obtaining a random movie by parsing the site animestars.org"""
    global list_of_title
    if len(dict_of_movies) == 0:
        response_get = requests.get(url=url)
        print(response_get.status_code)
        if response_get.status_code == 200:
            soup = bs(response_get.text, 'html.parser')  # запускаем парсер на сайт
            quotes_films = soup.find_all('a', class_="poster grid-item d-flex fd-column has-overlay")
            for film in quotes_films:
                link = film['href']
                name = film.div.img['alt']
                dict_of_movies[name] = link
            for key in dict_of_movies.keys():
                list_of_title.append(key)
            title = random.choice(list_of_title)
            return title, dict_of_movies[title]
        else:
            return None
    else:
        title = random.choice(list_of_title)
        return (title, dict_of_movies[title])

