# -*- coding: utf-8 -*
import sqlite3

class SQL:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_subscriber(self, user_id, place):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'Log_Request' ('user_id', 'place') VALUES(?,?)", (user_id, place))

    def top_place(self, user_id):
        """Определяем часто используемые города для пользователя"""
        with self.connection:
            my_rows_default = ['Волгоград', 'Москва', 'Лондон', 'Нью Йорк', 'Берлин']
            my_rows = []
            sql = f"""Select top_places.my_place as TOP5
            from (select place as my_place, count(*) as my_count
            from Log_Request
            where user_id = '{str(user_id)}'
            group by place
            order by 2 DESC) top_places limit 5"""
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for row in rows:
                my_rows.append(row[0])
                if row[0] in my_rows_default:#Удаляем город из списка поумочанию если он есть в топе у пользователя
                    my_rows_default.remove(row[0])
            my_rows = my_rows + my_rows_default
            return my_rows

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

