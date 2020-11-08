# -*- coding: utf-8 -*

word = 'end'
text = (f'First string { word }\n'
        'second string')
print(text)

# f'''Погода в городе { place }: { w.detailed_status }
# Температура воздуха: { round(w.temperature('celsius')['temp']) }C\xb0
# Давление: { w.humidity }мм рт. ст.
# Ветер { deg_word(w.wind()['deg']) } { w.wind()['speed'] } м/с'''
#
# f'''Погода в городе { place }: { weather_status }
# Температура воздуха: { temperature_air }C\xb0
# Давление: { humidity }мм рт. ст.
# Ветер { wind_direction } { wind_speed } м/с'''
