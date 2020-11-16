# -*- coding: utf-8 -*-
import telebot
from telebot import types
from weather import weather_answer, weather_tomorrow
from handler import add_log_string, add_subscription, top5_place, top5_place_user

#Инициализация бота
bot = telebot.TeleBot("1277471589:AAGLrKSri3RxwW03Yw_kvx0r8pgUpdUtrE8")

#Создаем клавиатуры
def top5_place_for_key(user_id):
    """Формирует избранные города на основе топов пользователя,
    всех пользователейи топа по-умолчанию"""
    top5_default = ('Москва', 'Санкт Петербург', 'Минск', 'Киев', 'Нур-Султан')
    return (top5_place_user(user_id) + tuple(i for i in top5_place() if i not in top5_place_user(user_id)) +
            tuple(i for i in top5_default if i not in top5_place_user(user_id) + top5_place()))[:5]

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


#РАБОТА С БОТОМ
#Обработка комнатды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open('static/welcome.webp', 'rb') as sti:
        bot.send_sticker(message.chat.id, sti)
    first_message = f"Добро пожаловать, {message.from_user.first_name}!\n Я - <b>{bot.get_me().first_name}</b>, бот " \
                    f"показывающий погоду по всему миру!\n Введите название города, погода в котором вас интересует."
    bot.send_message(message.chat.id, text=first_message, parse_mode='html',
                     reply_markup=create_reply_keybord(message.from_user.id))

#Обработка текстового сообщения
@bot.message_handler(content_types=['text'])
def send_weather(message):
    place = str.title(message.text)
    answer = weather_answer(place)
    print(place)
    if answer == 'Place error':
        bot.send_message(message.chat.id, "Введен несущестующий город. Попробуйте еще раз!")
    else:
        bot.send_message(message.chat.id, answer, reply_markup=create_inline_keybord(place))
        bot.send_message(message.chat.id, text='Какой еще город вам интересен?',
                         reply_markup=create_reply_keybord(message.from_user.id))
        add_log_string(user_id=message.from_user.id, place=place)

#Обработка inline кнопок
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    try:
        place = call.data[1:]
        if call.message:
            if int(call.data[0]) == 1:
                answer = weather_answer(place)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=answer, reply_markup=create_inline_keybord(place))
            elif int(call.data[0]) == 2:
                answer = weather_tomorrow(place)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=answer, reply_markup=create_inline_keybord(place))
            elif int(call.data[0]) == 3:
                add_subscription(user_id=call.message.chat.id, place=place)
                answer = f"Вы подписаны на получение погоды: {place}. Каждый вечер вы будите получать прогноз " \
                         f"на следующий день в этом месте"
                bot.send_message(call.message.chat.id, text=answer, reply_markup=create_reply_keybord(call.message.chat.id))
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=answer)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop = True)
