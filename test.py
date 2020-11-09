# -*- coding: utf-8 -*
from handler import top5_place, top5_place_user

def top5_place_for_key(user_id):
    """Формирует избранные города на основе топов пользователяб всех пользователей
     и топа по-умолчанию"""
    top5_default = ('Москва', 'Санкт Петербург', 'Минск', 'Киев', 'Нур-Султан')
    return (top5_place_user(user_id) + tuple(i for i in top5_place() if i not in top5_place_user(user_id)) +
            tuple(i for i in top5_default if i not in top5_place_user(user_id) + top5_place()))[:5]


print(top5_place_for_key('123456'))
