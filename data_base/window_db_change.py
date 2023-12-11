import tkinter as tk
from tkinter import ttk, messagebox
import random
import sqlite3
import constants

class WindowDBChange(object):
    def __init__(self, root, name_window: str = "Настройка диапазона") -> None:
        self.root = root
        self.modal_window = tk.Toplevel(self.root)
        self.modal_window.title(name_window)
        self.modal_window.geometry(f"400x300+600+200")

        self.frame_base = tk.Frame(self.modal_window)
        self.frame_base.pack(expand=1, fill='both')
        
        
        self.create_table()

        # Список элементов
        self.list_elements = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4"]

        # Виджеты интерфейса
        self.select_of_element = ttk.Combobox(self.frame_base, values=self.list_elements)
        self.select_of_element.set(self.list_elements[0])
        self.select_of_element.pack(pady=10)

        self.text_field = ttk.Entry(self.frame_base)
        self.text_field.pack(pady=10)

        self.button_write = ttk.Button(self.frame_base, text="Записать", command=self.set_to_bd)
        self.button_write.pack(pady=10)

        self.button_read = ttk.Button(self.frame_base, text="Прочитать", command=self.get_from_bd)
        self.button_read.pack(pady=10)
    
    def create_table(self):
        # Подключение к базе данных (если её нет, она будет создана)
        self.connection = sqlite3.connect(constants.PLACE_DB)
        self.cursor = self.connection.cursor()

        # Создание таблицы, если её нет
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS element (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                value INTEGER
            )
        """)

        self.connection.commit()

    def set_to_bd(self):
        element = self.select_of_element.get()
        value = self.text_field.get()

        # Запись в базу данных
        self.cursor.execute("INSERT INTO element (name, value) VALUES (?, ?)", (element, value))
        self.connection.commit()

    def get_from_bd(self):
        element = self.select_of_element.get()

        # Чтение из базы данных
        self.cursor.execute("SELECT value FROM elements WHERE name=?", (element,))
        rezult = self.cursor.fetchone()

        if rezult:
            print(f"Значение для {element}: {rezult[0]}")
        else:
            print(f"Нет данных для {element}")