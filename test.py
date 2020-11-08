# -*- coding: utf-8 -*

word = 'end'
text = f'''
First string { word }
second string'''
print(text)

f'''Погода в городе { place }: { weather_status }
Температура воздуха: { temperature_air }C\xb0
Давление: { humidity }мм рт. ст.
Ветер { wind_direction } { wind_speed } м/с'''

answer = "Погода в городе " + place + ": " + w.detailed_status + "\n"
answer += "Температура воздуха: " + str(round(w.temperature('celsius')['temp'])) + " C\xb0" + "\n"
answer += "Давление: " + str(w.humidity) + " мм рт. ст." + "\n"
deg = w.wind()['deg']
answer += "Ветер " + deg_word(deg) + " " + str(w.wind()['speed']) + " м/с" + "\n"