# -*- coding: utf-8 -*-
#Инициализация погоды
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
import apikeys

config_dict = get_default_config()
config_dict['language'] = 'ru'  # your language here
owm = OWM(apikeys.owm_apikey)  # You MUST provide a valid API key

#РАБОТА С ПОГОДОЙ
#Переводим показатель "Напрвление ветра" из градусов в читаемый формат
def deg_word(deg:int) ->str:
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
        return 'Place error'
    else:
        return (
            f"Погода в городе {place}: {weather_in_place.detailed_status}\n"
            f"Температура воздуха: {round(weather_in_place.temperature('celsius')['temp'])} C\xb0\n"
            f"Давление: {weather_in_place.humidity}мм рт. ст.\n"
            f"Ветер {deg_word(weather_in_place.wind()['deg'])} {weather_in_place.wind()['speed']} м/с."
        )


#Погода на завтра
def weather_tomorrow(place:str) ->str:
    """Формирует ответ с погодой на завтрав городе с названием 'place'
    в случае если город отсутствует выдет соответствующую информационную строку"""
    mgr = owm.weather_manager()
    try:
        forecaster = mgr.forecast_at_place(place, '3h')
    except:
        return 'Place error'
    else:
        answer = f"Прогноз погоды в городе {place} на завтра:\n"
    for time in [9, 12, 15, 18, 21]:
        tomorrow_time =  timestamps.tomorrow(time, 0)
        weather_in_time = forecaster.get_weather_at(tomorrow_time)
        answer +=  (
            f"В {time}-00: {weather_in_time.detailed_status}, "
            f"t\xb0: {round(weather_in_time.temperature('celsius')['temp'])} C\xb0, "
            f"h: {weather_in_time.humidity} мм рт. ст., "
            f"ветер {deg_word(weather_in_time.wind()['deg'])} {weather_in_time.wind()['speed']} м/с.\n"
        )
    return answer