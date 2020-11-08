# -*- coding: utf-8 -*-
#Инициализация погоды
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'  # your language here
owm = OWM('712128c315bc1ea671afb8f073ef8f85')  # You MUST provide a valid API key

#Инициализация бота
import telebot
from telebot import types
bot = telebot.TeleBot("1277471589:AAGLrKSri3RxwW03Yw_kvx0r8pgUpdUtrE8")

#Инициализация базы
from sql import SQL
db = SQL('db.db')

time_key = []
for i in range(1, 25):
    time_key.append(str(i) + '-00')

#РАБОТА С ПОГОДОЙ
#Переводим показатель "Напрвление ветра" из градусов в читаемый формат
def deg_word(deg):
    """Преобразует направление ветра в градусах в строку типа 'северный', 'северо-западный' и так далее."""
    if (0 <= deg < 45) or (315 < deg <= 360):
        deg_str = "северный"
    elif deg == 45:
        deg_str = "северо-восточный"
    elif 45 < deg < 135:
        deg_str = "восточный"
    elif deg == 135:
        deg_str = "юго-восточный"
    elif 135 < deg < 225:
        deg_str = "южный"
    elif deg == 225:
        deg_str = "юго-западный"
    elif  225 < deg < 315:
        deg_str = "западный"
    elif deg == 315:
        deg_str = "северо-западный"
    else:
        deg_str = "направление не известно"
    return deg_str
#Погода на текущий момент
def weather_answer(place:str) ->str:
    """Формирует ответ с текущей погодой в городе с названием 'place'
    в случае если город отсутствует выдет соответствующую информационную строку"""
    mgr = owm.weather_manager()
    try:
        weather_in_place = mgr.weather_at_place(place).weather
    except:
        return "Введен несущестующий город. Попробуйте еще раз!"
    else:
        return (
            f"Погода в городе {place}: {weather_in_place.detailed_status}\n"
            f"Температура воздуха: {round(weather_in_place.temperature('celsius')['temp'])} C\xb0\n"
            f"Давление: {weather_in_place.humidity}мм рт. ст.\n"
            f"Ветер {deg_word(weather_in_place.wind()['deg'])} {weather_in_place.wind()['speed']} м/с."
        )


#Погода на завтра
def weather_tomorrow(place):
    mgr = owm.weather_manager()
    if True:
        try:
            forecaster = mgr.forecast_at_place(place, '3h')
        except:
            answer = "Введен несущестующий город. Попробуйте еще раз!"
        else:
            answer = "Прогноз погоды в городе " + str.title(place) + " на завтра:"+ "\n"
        for time in [9, 12, 15, 18, 21]:
            tomorrow_time =  timestamps.tomorrow(time, 0)
            w = forecaster.get_weather_at(tomorrow_time)
            answer_str = "В " + str(time) + "-00: " + w.detailed_status
            answer_str += ", t\xb0: " + str (round(w.temperature('celsius')['temp'])) + " C\xb0"
            answer_str += ", h: " + str(w.humidity) + " мм рт. ст."
            deg = w.wind()['deg']
            answer_str += ", ветер " + deg_word(deg) + " " + str(w.wind()['speed']) + " м/с" + "\n"
            answer += answer_str

    return answer


#РАБОТА С БОТОМ

#Обработка комнатды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
#Создаем клавиатуру
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, бот показывающий погоду по всему миру!\n Введите название города, погода в котором вас интересует.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=create_reply_keybord(message.from_user.id))

#Обработка текстового сообщения
@bot.message_handler(func=lambda message: message.text in time_key and message.content_type == 'text')
def sub_time(message):
    answer = "Да ладно!"
    bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=['text'])
def send_weather(message):
    place = str.title(message.text)
    answer = weather_answer(place)
    print(place)
    if answer == "Введен несущестующий город. Попробуйте еще раз!":
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, answer, reply_markup=create_inline_keybord(place))
        bot.send_message(message.chat.id, text='Какой еще город вам интересен?',  reply_markup=create_reply_keybord(message.from_user.id))
        db.add_subscriber(user_id=message.from_user.id, place=place)


#Обработка inline кнопок
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    try:
        place = call.data[1:]
        if call.message:
            if int(call.data[0]) == 1:
                answer = weather_answer(place)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=create_inline_keybord(place))
            elif int(call.data[0]) == 2:
                answer = weather_tomorrow(place)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=create_inline_keybord(place))
            elif int(call.data[0]) == 3:
                sub(chat_id=call.message.chat.id, place=place)
                answer = weather_tomorrow(place)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=create_clock_keybord())

    except Exception as e:
        print(repr(e))


# Подписка
def sub(chat_id, place):
    answer = 'Выберите удобное время для получения прогноза погоды на завтра в городе ' + place
    bot.send_message(chat_id, answer, reply_markup=create_clock_keybord())


#Клавиатура
def create_inline_keybord(place):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Сегодня", callback_data=str(1) + place)
    item2 = types.InlineKeyboardButton("Завтра", callback_data=str(2) + place)
    item3 = types.InlineKeyboardButton("Подписаться", callback_data=str(3) + place)
    markup.add(item1, item2)
    markup.add(item3)
    return markup

def create_reply_keybord(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    top_place = db.top_place(str(user_id))
    item1 = types.KeyboardButton(top_place[0])
    item2 = types.KeyboardButton(top_place[1])
    item3 = types.KeyboardButton(top_place[2])
    item4 = types.KeyboardButton(top_place[3])
    item5 = types.KeyboardButton(top_place[4])
    markup.add(item1, item2, item3, item4, item5)
    return markup

def create_clock_keybord():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('1-00','2-00','3-00','4-00','5-00','6-00')
    markup.row('7-00','8-00','9-00','10-00','11-00','12-00')
    markup.row('13-00','14-00','15-00','16-00','17-00','18-00')
    markup.row('19-00','20-00','21-00','22-00','23-00','24-00')
    return markup


bot.polling(none_stop = True)
