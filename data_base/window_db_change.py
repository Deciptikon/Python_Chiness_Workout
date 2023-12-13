import tkinter as tk
from tkinter import ttk, messagebox
import random
import constants
from modal_windows.class_modal_window import ModalWindow
from data_base.class_db import DataBase

class WindowDBChange( ModalWindow, DataBase, object):
    def __init__(self, root, name_window: str = "Настройка диапазона", geometry: str = '400x300+600+200') -> None:
        ModalWindow.__init__(self=self, root=root, name_window=name_window, geometry=geometry)
        DataBase.__init__(self=self, place_db=constants.PLACE_DB)
        
        #print('--------->')
        self.frame_base = tk.Frame(self.modal_window)
        self.frame_base.pack(expand=1, fill='both')
        
        #print('--------->')
        #self.create_table()

        # Список элементов
        self.list_elements = ["Элемент 1", "Элемент 2", "人", "Элемент 4"]

        # Виджеты интерфейса
        self.select_of_element = ttk.Combobox(self.frame_base, values=self.list_elements)
        self.select_of_element.set(self.list_elements[0])
        self.select_of_element.pack(pady=10)

        self.text_field = ttk.Entry(self.frame_base)
        self.text_field.pack(pady=10)

        self.button_write = ttk.Button(self.frame_base, text="Записать", command=self.write_to_db)
        self.button_write.pack(pady=10)

        self.button_read = ttk.Button(self.frame_base, text="Прочитать", command=self.read_from_db)
        self.button_read.pack(pady=10)
        
        self.modal_window.transient(self.root)
        self.modal_window.wait_window(self.modal_window)
        
    def write_to_db(self):
        element = self.select_of_element.get()
        value = self.text_field.get()
        print("Записать")
        #self.set_to_bd(element=element, value=value)
        self.intellectual_update(element=element, value=value)
        print("Записано!")
    
    def read_from_db(self):
        element = self.select_of_element.get()
        rezult = self.get_from_bd(element=element)
        self.text_field.delete(0, tk.END)
        if rezult:
            print(f"Значение для {element}: {rezult[0]}")
            
            self.text_field.insert(0, str(rezult[0]))
        else:
            print(f"Значение для {element}:   ")
    
    