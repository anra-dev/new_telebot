from peewee import IntegrityError, fn
from models import TelegramUser, LogRequest


def add_telegram_user(user_id):
    row = TelegramUser(
        user_id=user_id,
    )
    row.save()

def add_log_string(user_id, place):
    try:
        add_telegram_user(user_id)
    except IntegrityError as de:
        pass
    telegram_user = TelegramUser.select().where(TelegramUser.user_id == user_id).get()
    row = LogRequest(
        telegram_user=telegram_user,
        place=place.title().strip(),
    )
    row.save()

def add_subscription(user_id, place):
    telegram_user = TelegramUser.get(TelegramUser.user_id == user_id)
    telegram_user.subscription = place.title().strip()
    telegram_user.save()

def del_subscription_all(user_id):
    pass

def del_subscription(user_id, place):
    pass

def top5_place():
    query = (LogRequest
             .select(LogRequest.place, fn.COUNT(LogRequest.place))
             .where(LogRequest.place.is_null(False))
             .group_by(LogRequest.place)
             .order_by(fn.COUNT(LogRequest.place).desc())
             .limit(5))
    return tuple(map(lambda item: item.place, query))

def top5_place_user(user_id):
    telegram_user = TelegramUser.get(TelegramUser.user_id == user_id)
    query = (LogRequest
             .select(LogRequest.place, fn.COUNT(LogRequest.place))
             .where(LogRequest.telegram_user == telegram_user)
             .group_by(LogRequest.place)
             .order_by(fn.COUNT(LogRequest.place).desc())
             .limit(5))
    return tuple(map(lambda item: item.place, query))


if __name__ == '__main__':
    print(top5_place_user('123458'))
    print(top5_place())
    print((top5_place_user(123458) + top5_place())[:5])
    # add_log_string('123457', 'волгоград')
    # add_log_string('123457', 'волгоград')
    # add_log_string('123457', 'саратов')
    # add_log_string('123457', 'ростов')
    # add_log_string('123457', 'москва')
    # add_log_string('123457', 'волгоград')
    # add_log_string('123457', 'саратов')
    # add_log_string('123457', 'ростов')
    # add_log_string('123457', 'москва')
    # add_log_string('123457', 'саратов')
    # add_log_string('123457', 'ростов')
    # add_log_string('123458', 'сургут')
    # add_log_string('123458', 'тува')
    # add_log_string('123458', 'тува')
    # add_log_string('123458', 'ростов')
