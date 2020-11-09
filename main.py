# -*- coding: utf-8 -*-

import telebot
from telebot import types
from weather import weather_answer, weather_tomorrow
from handler import add_log_string, add_subscription, top5_place, top5_place_user
#Инициализация бота
bot = telebot.TeleBot("1277471589:AAGLrKSri3RxwW03Yw_kvx0r8pgUpdUtrE8")




def top5_place_for_key(user_id):
    """Формирует избранные города на основе топов пользователя,
    всех пользователейи топа по-умолчанию"""
    top5_default = ('Москва', 'Санкт Петербург', 'Минск', 'Киев', 'Нур-Султан')
    return (top5_place_user(user_id) + tuple(i for i in top5_place() if i not in top5_place_user(user_id)) +
            tuple(i for i in top5_default if i not in top5_place_user(user_id) + top5_place()))[:5]

#РАБОТА С БОТОМ
#Обработка комнатды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
#Создаем клавиатуру
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, бот показывающий погоду по всему миру!\n Введите название города, погода в котором вас интересует.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=create_reply_keybord(message.from_user.id))

# #Обработка текстового сообщения
# @bot.message_handler(func=lambda message: message.text in time_key and message.content_type == 'text')
# def sub_time(message):
#     answer = "Да ладно!"
#     bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=['text'])
def send_weather(message):
    place = str.title(message.text)
    answer = weather_answer(place)
    print(place)
    if answer == 'Place error':
        bot.send_message(message.chat.id, "Введен несущестующий город. Попробуйте еще раз!")
    else:
        bot.send_message(message.chat.id, answer, reply_markup=create_inline_keybord(place))
        bot.send_message(message.chat.id, text='Какой еще город вам интересен?',  reply_markup=create_reply_keybord(message.from_user.id))
        add_log_string(user_id=message.from_user.id, place=place)

#Обработка inline кнопок
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    try:
        place = call.data[1:]
        if call.message:
            if int(call.data[0]) == 1:
                answer = weather_answer(place)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=answer, reply_markup=create_inline_keybord(place))
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
    keys_name = top5_place_for_key(user_id)
    item1 = types.KeyboardButton(keys_name[0])
    item2 = types.KeyboardButton(keys_name[1])
    item3 = types.KeyboardButton(keys_name[2])
    item4 = types.KeyboardButton(keys_name[3])
    item5 = types.KeyboardButton(keys_name[4])
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
