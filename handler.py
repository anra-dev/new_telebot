
import peewee
from peewee import IntegrityError
from models import TelegramUser, LogRequest


def add_telegram_user(user_id):
    row = TelegramUser(
        user_id=user_id.lower().strip(),
    )
    row.save()


def add_log_string(user_id, place):
    try:
        add_telegram_user(user_id)
    except IntegrityError as de:
        pass
    telegram_user = TelegramUser.select().where(TelegramUser.user_id == user_id.strip()).get()
    row = LogRequest(
        telegram_user=telegram_user,
        place=place.lower().strip(),
    )
    row.save()


if __name__ == '__main__':
    add_log_string('1321423', 'Москва')
    add_log_string('1321423', 'ВОлгоград')
    add_log_string('1321424', 'Москва')
    add_log_string('1321425', 'Москва')
    add_log_string('1321423', 'Москва')