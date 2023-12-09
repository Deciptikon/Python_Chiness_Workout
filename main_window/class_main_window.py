import tkinter as tk
from tkinter import ttk, filedialog
import random

import constants 
from test_machine.class_test_machine import TestMachine
from brain_machine.class_brain_machine import BrainMachine
from window_diapasone.class_window_diapasone import WindowDiapasone

class MainWindow(object):
    # счёт правильных ответов
    data_score_positive: int = 0

    # счёт НЕправильных ответов
    data_score_negative: int = 0

    # скрытвй параметр, номер верного ответа
    true_answer: int = 0

    # скрытый параметр, первый ход, первое нажатие
    first_step: bool = True

    # Массивы содержащие распарсенный словарь
    russ_words: list[str] = []
    chin_words: list[str] = []

    def __init__(self, root) -> None:
        self.root = root

        self.root.title(f'{constants.NAME_PROGRAM} {constants.VERSION}')
        self.root.iconbitmap(default='icon.ico')
        #root.attributes("-alpha", 0.5)
        self.root.geometry("1000x600+400+200")

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TNotebook.Tab', background="White")
        self.style.map("TNotebook", background= [("selected", "White")])

        file_content = self.read_file('chinese_dict.txt') #"Words.txt"
        self.russ_words, self.chin_words = self.parse_dictonary(file_content)

        # Создаем меню  ############################################################

        self.menu_bar = tk.Menu(self.root)

        # Создаем подменю "Файл" ###################################################
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Открыть", command=self.on_open_file)
        #file_menu.add_command(label="Сохранить", command=on_menu_click)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выход", command=self.root.destroy)
        # Добавляем подменю "Файл" к основному меню 
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)

        # Создаем подменю "Правка" #################################################
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Диапазон", command=self.on_diapason_words)

        # Добавляем подменю "Правка" к основному меню
        self.menu_bar.add_cascade(label="Правка", menu=self.edit_menu)

        # Создаем подменю "Помощь" #################################################
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="О программе", command=self.on_about_program)

        # Добавляем подменю "Помощь" к основному меню
        self.menu_bar.add_cascade(label="Помощь", menu=self.help_menu)

        # Устанавливаем основное меню для главного окна
        self.root.config(menu=self.menu_bar)

        # Создаем виджет вкладок ###################################################
        self.notebook = ttk.Notebook(self.root)

        ############################################################################
        # Вкладка 1
        self.t1 = TestMachine(window=self.root, 
                              notebook=self.notebook, 
                              russ_dict=self.russ_words, 
                              chin_dict=self.chin_words)

        ############################################################################
        # Вкладка 2
        self.t2 = BrainMachine(window=self.root, 
                               notebook=self.notebook, 
                               russ_dict=self.russ_words, 
                               chin_dict=self.chin_words)

        ############################################################################
        # Вкладка 3

        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text=' Адаптивный ')

        self.frame_base3 = tk.Frame(self.tab3)
        self.frame_base3.pack(expand=1, fill='both')

        ############################################################################

        self.notebook.pack(expand=1, fill='both')
        self.root.bind('<space>', self.space_event)

        self.on_diapason_words()



    # Процедура открытия окна с информацией о программе
    def on_about_program(self):
        print('About ....')
        self.open_about_window()

    # Открывает меню выбора нового словаря
    def on_open_file(self):
        self.russ_words
        self.chin_words
        print('Open Fire, sorry... File')
        file_path = filedialog.askopenfilename(title='Open Fire, sorry... File', 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            print(f"Выбранный файл: {file_path}")
    
        file_content = self.read_file(file_path)
        self.russ_words, self.chin_words = self.parse_dictonary(file_content)

        self.t1.set_dicts(russ_dict=self.russ_words, chin_dict=self.chin_words)
        self.t2.set_dicts(russ_dict=self.russ_words, chin_dict=self.chin_words)



    def on_diapason_words(self):
        diap_window = WindowDiapasone(root=self.root, 
                                      tab1=self.t1,
                                      tab2=self.t2,
                                      russ_dict=self.russ_words,
                                      chin_dict=self.chin_words)


    # Открывает модальное окно с информацией о программе
    def open_about_window(self):
        self.modal_window = tk.Toplevel(self.root)
        self.modal_window.title("О программе")
        self.modal_window.geometry("400x350+650+200")
        self.label = tk.Label(self.modal_window, 
                        text=F"""Это простой тренер китайского языка.

В нём имеются 3 режима обучения:
 - на основе тестирования;                            
 - на сонове памяти;                                      
 - на основе адаптированного подбора слов;
 
 Текущая версия программы {constants.VERSION}
 
 Программа абсолютно бесплатна ;-)



 Адрес для связи по любым ВАЖНЫМ вопросам:
 email: deciptikon@mail.ru
 
 """)
    
        self.label.pack(padx=20, pady=20)
        # Устанавливаем родительское окно для модального окна
        self.modal_window.transient(self.root)
        # Ожидаем закрытия модального окна перед возвращением к основному окну
        self.modal_window.wait_window(self.modal_window)

    def parse_dictonary(self, file_dictonary: str) -> [list[str], list[str]]:
        russ: list[str] = []
        chin: list[str] = []
        for line in file_dictonary.split('\n'):
            if len(line.strip()) > 0:
                c,r = line.split(' : ')
                russ.append(self.cut_str(long_str=r, max_len=50, slice_symbol=','))
                chin.append(c)
        return russ, chin
    
    # Действие при нажатии на Space
    def space_event(self, event):
        print('SPACE -->')
        index_tab = self.notebook.index(self.notebook.select())
        match index_tab:
            case 0:
                self.t1.on_button_next()
            case 1:
                if not self.t2.first_step:
                    self.t2.on_button_next()
            case 2:
                pass

    # генерируем несколько различных целых чисел
    def generate_random_indexes(self, min: int = 0, max: int = 7, num: int = 4) -> list[int]:
        return random.sample(range(min, max + 1), num)

    # Сокращает строку до ближайшего символа slice_symbol с конца, 
    # причём длина строки не будет превышать max_len
    def cut_str(self, long_str: str = '', max_len: int = 50, slice_symbol: str = ','):
        slices_str = long_str.split(slice_symbol)
        short_str = ''
        for s in slices_str:
            if len(short_str + s) < max_len:
                short_str += s + slice_symbol
            else:
                break
        return short_str[:len(short_str)-1]

    # Открытие файла
    def read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка чтения файла: {e}"