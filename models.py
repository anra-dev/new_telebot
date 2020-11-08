from datetime import datetime
from peewee import SqliteDatabase, Model
from peewee import CharField, PrimaryKeyField, DateTimeField, ForeignKeyField

sqlite_db = SqliteDatabase('app.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})

class BaseModel(Model):
    class Meta:
        database = sqlite_db


class TelegramUser(BaseModel):
    id = PrimaryKeyField(null=False)
    user_id = CharField(max_length=100, unique=True)
    subscription = CharField(max_length=100, null=True)

    class Meta:
        db_table = "telegram_user"
        order_by = ('id',)


class LogRequest(BaseModel):
    id = PrimaryKeyField(null=False)
    time_request = DateTimeField(default=datetime.now())
    telegram_user = ForeignKeyField(TelegramUser, backref='request')
    place = CharField(max_length=100)

    class Meta:
        db_table = "log_request"
        order_by = ('time_request',)
