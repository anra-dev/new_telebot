import peewee
from models import *

if __name__ == '__main__':
    try:
        sqlite_db.connect()
        TelegramUser.create_table()
    except peewee.InternalError as px:
        print(str(px))
    try:
        LogRequest.create_table()
    except peewee.InternalError as px:
        print(str(px))

