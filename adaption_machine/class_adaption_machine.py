from tkinter import ttk
import random
import sqlite3

from test_machine.class_test_machine import TestMachine

class AdaptionMachine(TestMachine, object):
    def __init__(self, window, notebook, russ_dict: list[str], chin_dict: list[str], nameTab=' *** '):
        super().__init__(window, notebook, russ_dict, chin_dict, nameTab)
        
        #
    
    # Переопределяем функцию генерации случайных индексов в диапахоне
    # Теперь она должна учитывать показатели угадывания числа
    def generate_random_indexes(self, min: int = 0, max: int = 7, num: int = 4) -> list[int]:
        return random.sample(range(min, max + 1), num)
    
    