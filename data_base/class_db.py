import sqlite3
import os.path

class DataBase:
    def __init__(self, place_db: str = '') -> None:
        print('--------->')
        self.connection = None
        self.create_table(place_db=place_db)
        
    def create_table(self, place_db: str = '') -> None:
        # Подключение к базе данных (если её нет, она будет создана)
        self.connection = sqlite3.connect(place_db)
        self.cursor = self.connection.cursor()
        # Создание таблицы, если её нет
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS elements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                value INTEGER
            )
        """)
        self.connection.commit()

    def intellectual_update(self, element, value) -> None:
        if self.get_from_bd(element):
            self.update_element(element, value)
        else:
            self.set_to_bd(element, value)
            
    def update_element(self, element, value) -> None:
        self.cursor.execute("UPDATE elements SET value = ? WHERE name = ?", (value, element))
        self.connection.commit()
    
    # Запись в базу данных
    def set_to_bd(self, element, value) -> None:
        print(f'Записываем {value=} в {element=}')
        self.cursor.execute("INSERT INTO elements (name, value) VALUES (?, ?)", (element, value))
        self.connection.commit()
    
    # Чтение из базы данных
    def get_from_bd(self, element) -> list:
        self.cursor.execute("SELECT value FROM elements WHERE name=?", (element,))
        rezult = self.cursor.fetchone()
        return rezult