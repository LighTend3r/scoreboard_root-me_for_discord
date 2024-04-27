import sqlite3
import os
from utils.metaclass import SingletonMeta

create_db_querry = open('bot.sql', 'r').read()
DATABASE_PATH = 'databases/bot.db'

def init_db():
    if not os.path.exists('databases'):
        os.makedirs('databases')

    if os.path.exists(DATABASE_PATH):
        return

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executescript(create_db_querry)
    conn.commit()
    conn.close()


class Dabatase(metaclass=SingletonMeta):
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()


    @staticmethod
    def get_cursor():
        return Dabatase().cursor
