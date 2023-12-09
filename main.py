import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from transitions import Machine
import random

VERSION = '0.3.2'
NAME_PROGRAM = 'Chinese Trainer'

COLOR_GREEN = "#00AA55"
COLOR_RED   = "#AA2222"
COLOR_GRAY  = "#DDDDDD"

font_big   = ("Arial", 100)  
font_small = ("Arial", 18)  
font_score = ("Arial", 30) 

class BaseTab:
    def __init__(self, window, notebook, russ_dict: list[str], chin_dict: list[str]):
        self.window = window
        self.notebook = notebook
        self.russ_words = russ_dict
        self.chin_words = chin_dict
        self.selected_tab = 0
        self.window.bind('<Return>', self.enter_event)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def set_dicts(self, russ_dict: list[str], chin_dict: list[str]):
        self.russ_words = russ_dict
        self.chin_words = chin_dict

    # Действие нажатия на Enter
    def enter_event(self, event):
        pass

    # Действие при смене вкладки
    def on_tab_changed(self, event):
        self.selected_tab = self.notebook.index(self.notebook.select())
        print(f"Активная вкладка: {self.selected_tab}")
        self.window.focus_set()

# Class TestMachine ######################################################################
class TestMachine(BaseTab, object):
    true_answer: int = 0
    first_step: bool = True
    data_score_positive: int = 0
    data_score_negative: int = 0
    num_button = None

    def __init__(self, window, notebook, russ_dict: list[str], chin_dict: list[str]):
        super().__init__( window, notebook, russ_dict, chin_dict)
        states_test_machine = ['Basic', 'Answer', 'True_answer', 'False_answer']
        transitions_test_machine = [
            {'trigger': 'check', 'source': 'Basic', 'dest': 'Answer'},
            {'trigger': 'true', 'source': 'Answer', 'dest': 'True_answer'},
            {'trigger': 'false', 'source': 'Answer', 'dest': 'False_answer'},
            {'trigger': 'check', 'source': ['True_answer', 'False_answer'], 'dest': 'Answer'},
            {'trigger': 'next', 'source': ['True_answer', 'False_answer'], 'dest': 'Basic'},
            {'trigger': 'next', 'source': 'Basic', 'dest': 'Basic'}
        ]
        self.machine = Machine(model=self, 
                              states=states_test_machine, 
                              transitions=transitions_test_machine, 
                              initial='Basic')

        self.tab = ttk.Frame(self.notebook)
        self.notebook.add(self.tab, text=' Тестовый ')

        self.frame_base = tk.Frame(self.tab)
        self.frame_base.pack(expand=1, fill='both')

        self.label_text = tk.Label(self.frame_base, text="[***]", font=font_big)
        self.label_text.pack(pady=10)

        self.label_score_positive = tk.Label(self.frame_base, text=f'+{self.data_score_positive}', font=font_score)
        self.label_score_positive.place(x = 10, y = 50)

        self.label_score_negative = tk.Label(self.frame_base, text=f' -{self.data_score_negative}', font=font_score)
        self.label_score_negative.place(x = 10, y = 100)

        self.frame = tk.Frame(self.frame_base)
        self.frame.pack(side=tk.TOP, pady=10)

        self.buttons = []
        for i in range(1, 5):
            self.button = tk.Button(self.frame, text=f"****", 
                                command=lambda num=i-1: self.on_button_click(num), 
                                font=font_small, 
                                padx=10,
                                width=50)
            self.button.grid(row=i-1, column=0, pady=10, padx=10 )
            self.window.bind(str(i), self.num_event)
            self.buttons.append(self.button)

        self.button_next = tk.Button(self.tab, text=f"Next", 
                                command=lambda: self.on_button_next(), 
                                font=font_small, 
                                width=200, height=50,
                                bg='#DDDDDD')
        self.button_next.pack(side=tk.RIGHT, anchor=tk.SE)
        self.next()


    def on_enter_Basic(self):
        print("State = Basic")
        self.num_button = None
        self.first_step = True
        indexes = generate_random_indexes(max=len(self.russ_words)-1)
        print(indexes)
        self.true_answer = random.randint(0, 3)
        print(self.true_answer)
        ind = indexes[self.true_answer]
        self.label_text.config(text=self.chin_words[ind])
        i: int = 0
        for button in self.buttons:
            ind = indexes[i]
            button.config(text=self.russ_words[ind], bg=COLOR_GRAY)
            i += 1

    # Callback-метод, вызываемый при входе в состояние Answer
    def on_enter_Answer(self):
        print("State = Answer")
        if self.num_button == self.true_answer:
            self.true()
        else:
            self.false()

    # Callback-метод, вызываемый при входе в состояние True_answer
    def on_enter_True_answer(self):
        print("State = True_answer")
        bt = self.buttons[self.num_button]
        bt.config(bg=COLOR_GREEN)
        if self.first_step:
            self.data_score_positive += 1
            self.label_score_positive.config(text=f'+{self.data_score_positive}')
        self.first_step = False

    # Callback-метод, вызываемый при входе в состояние False_answer
    def on_enter_False_answer(self):
        print("State = False_answer")
        bt = self.buttons[self.num_button]
        bt.config(bg=COLOR_RED)
        if self.first_step:
            self.data_score_negative += 1
            self.label_score_negative.config(text=f' -{self.data_score_negative}')
        self.first_step = False

    # Действие 4-х кнопок на первой вкладке (режим Тестовый)
    def on_button_click(self, button_number):
        print(f'---> click --> {button_number=}')
        self.num_button = button_number
        self.check()

    # Действие на первой вкладке (режим Тестирование)
    def on_button_next(self):
        self.next()

    # действия при нажатии на цифровые клавиши
    def num_event(self, event):
        if self.notebook.index(self.notebook.select()) == 0:
            print(event)
            i = int(event.keysym) - 1
            if i in range(0, 4):
                self.buttons[i].invoke()

# END Class TestMachine ######################################################################

# Class BrainMachine ######################################################################
class BrainMachine(BaseTab, object):
    true_answer: int = 0
    first_step: bool = True
    data_score_positive: int = 0
    data_score_negative: int = 0

    def __init__(self, window, notebook, russ_dict: list[str], chin_dict: list[str]):
        super().__init__( window, notebook, russ_dict, chin_dict)
        states_brain_machine = ['Basic', 'Answer', 'True_answer', 'False_answer']
        transitions_brain_machine = [
            {'trigger': 'check', 'source': 'Basic', 'dest': 'Answer'},
            {'trigger': 'true', 'source': 'Answer', 'dest': 'True_answer'},
            {'trigger': 'false', 'source': 'Answer', 'dest': 'False_answer'},
            {'trigger': 'check', 'source': ['True_answer', 'False_answer'], 'dest': 'Basic'},
            {'trigger': 'next', 'source': ['True_answer', 'False_answer'], 'dest': 'Basic'},
            {'trigger': 'next', 'source': 'Basic', 'dest': 'Basic'}
        ]
        self.machine = Machine(model=self, 
                              states=states_brain_machine, 
                              transitions=transitions_brain_machine, 
                              initial='Basic')
        
        self.tab = ttk.Frame(self.notebook)
        self.notebook.add(self.tab, text=' Письменный ')

        self.frame_base = tk.Frame(self.tab)
        self.frame_base.pack(expand=1, fill='both')

        self.label_text = tk.Label(self.frame_base, text="[***]", font=font_big)
        self.label_text.pack(pady=10)

        self.label_score_positive = tk.Label(self.frame_base, text=f'+{data_score_positive}', font=font_score)
        self.label_score_positive.place(x = 10, y = 50)

        self.label_score_negative = tk.Label(self.frame_base, text=f' -{data_score_negative}', font=font_score)
        self.label_score_negative.place(x = 10, y = 100)

        self.text_input = tk.Entry(self.frame_base, font=font_small, bg='#DDDDDD', width=200)
        self.text_input.pack(pady=10, padx=100)

        self.button_check = tk.Button(self.frame_base, text=f"Check", 
                                command=lambda: self.on_button_check(), 
                                font=font_small, 
                                width=200, #height=50,
                                bg='#DDDDDD')
        self.button_check.pack( pady=10, padx=50 )

        self.label_text_checker = tk.Label(self.frame_base, text="Введите перевод по памяти.\n", font=font_small)
        self.label_text_checker.pack(pady=50)

        self.button_next = tk.Button(self.tab, text=f"Next", 
                        command=lambda: self.on_button_next(), 
                        font=font_small, 
                        width=200, height=50,
                        bg='#DDDDDD')
        self.button_next.pack(side=tk.BOTTOM, anchor=tk.SE, pady=0)
        self.next()
    
    # Callback-метод, вызываемый при входе в состояние Basic
    def on_enter_Basic(self):
        self.true_answer = random.randint(0, len(self.russ_words)-1)
        print(self.true_answer)
        self.first_step = True
        self.label_text.config(text=self.chin_words[self.true_answer])
        self.text_input.delete(0, len(self.text_input.get()))
        self.button_check.config(bg=COLOR_GRAY)
        self.label_text_checker.config(text="Введите перевод по памяти.\n")

    # Callback-метод, вызываемый при входе в состояние Answer
    def on_enter_Answer(self):
        print("State = Answer")
        self.input_text_from_widget = self.text_input.get().split(',')
        self.true_words = self.russ_words[self.true_answer]
        for word in self.input_text_from_widget:
            #w = word.replace(' ','')
            w = word.strip()
            print(w)
            if len(w)>0 and w in self.true_words:
                if self.first_step:
                    self.true()
                    break
        if self.first_step:
            self.false()

    # Callback-метод, вызываемый при выходе из состояния Answer
    # Этот код для примера, в программе он не нужен. Но из-за того что я могу забыть о нём,
    # я оставил это здесь
    def on_exit_Answer(self):
        print("Вы вышли из состояния Answer")

    # Callback-метод, вызываемый при входе в состояние True_answer
    def on_enter_True_answer(self):
        print("State = True_answer")
        self.data_score_positive += 1
        self.first_step = False
        self.label_score_positive.config(text=f'+{self.data_score_positive}')
        self.button_check.config(bg=COLOR_GREEN)
        self.label_text_checker.config(text=f'ВЕРНО!!!\n\"{self.true_words}\"')

    # Callback-метод, вызываемый при входе в состояние False_answer
    def on_enter_False_answer(self):
        print("State = False_answer")
        self.data_score_negative += 1
        self.first_step = False
        self.label_score_negative.config(text=f'-{self.data_score_negative}')
        self.button_check.config(bg=COLOR_RED)
        self.label_text_checker.config(text=f'ОШИБКА, должно быть:\n\"{self.true_words}\"')

    # Действие кнопки Next на второй вкладке (режим письменный)
    def on_button_next(self):
        self.next()

    # Действие при нажатии на кнопку проверки (в письменном режиме)
    def on_button_check(self):
        self.check()

    def enter_event(self, event):
        if self.notebook.index(self.notebook.select()) == 1:
            self.button_check.invoke()
            print('ENTER')

# END Class BrainMachine ######################################################################

class WindowDiapasone(object):
    def __init__(self, root) -> None:
        self.root = root
        self.modal_window = tk.Toplevel(self.root)
        self.modal_window.title("Настройка диапазона")
        self.modal_window.geometry("300x300+650+200")

        self.frame_base = tk.Frame(self.modal_window)
        self.frame_base.pack(expand=1, fill='both')

        self.label_min = tk.Label(self.frame_base, text="Min", font=font_small)
        self.label_min.pack(pady=10)
        self.spin_value_min = tk.StringVar(value='0')
        self.spinbox_min = ttk.Spinbox(self.frame_base, 
                                       from_=0, to=len(russ_words)-1, 
                                       textvariable=self.spin_value_min)
        self.spinbox_min.pack()

        self.label_max = tk.Label(self.frame_base, text="Max", font=font_small)
        self.label_max.pack(pady=10)
        self.spin_value_max = tk.StringVar(value=f'{len(russ_words)-1}')
        self.spinbox_max = ttk.Spinbox(self.frame_base, 
                                       from_=0, to=len(russ_words)-1, 
                                       textvariable=self.spin_value_max)
        self.spinbox_max.pack()

        self.button_ok = ttk.Button(self.frame_base, text="Ok", 
                           command=self.on_button_ok_diapason)
        self.button_ok.pack(side="left", padx=10, expand=1)

        self.button_cancel = ttk.Button(self.frame_base, text="Отмена", 
                               command=self.modal_window.destroy)
        self.button_cancel.pack(side="left", padx=10, expand=1)

        # Устанавливаем родительское окно для модального окна
        self.modal_window.transient(self.root)
        # Ожидаем закрытия модального окна перед возвращением к основному окну
        self.modal_window.wait_window(self.modal_window)


    def on_button_ok_diapason(self):

        min_value = int(self.spinbox_min.get())
        max_value = int(self.spinbox_max.get())
        raz: int = 4
        print(f'Minimum = {self.spinbox_min.get()}')
        print(f'Maximum = {self.spinbox_max.get()}')
        if max_value - min_value < raz:
            messagebox.showinfo("Внимание", f"Максимальное значение должно превышать минимальное более чем на {raz} единиц.")
        else:
            russ_cuting = russ_words[min_value:max_value+1]
            chin_cuting = chin_words[min_value:max_value+1]
            t1.set_dicts(russ_dict=russ_cuting, chin_dict=chin_cuting)
            t2.set_dicts(russ_dict=russ_cuting, chin_dict=chin_cuting)
            messagebox.showinfo("Успешно", f"Диапазон от {min_value} до {max_value} успешно установлен")
            self.modal_window.destroy()



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

        self.root.title(f'{NAME_PROGRAM} {VERSION}')
        self.root.iconbitmap(default='icon.ico')
        #root.attributes("-alpha", 0.5)
        self.root.geometry("1000x600+400+200")

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TNotebook.Tab', background="White")
        self.style.map("TNotebook", background= [("selected", "White")])

        file_content = self.read_file('chinese_dict.txt') #"Words.txt"
        self.russ_words, self.chin_words = parse_dictonary(file_content)

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
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Диапазон", command=on_diapason_words)

        # Добавляем подменю "Правка" к основному меню
        menu_bar.add_cascade(label="Правка", menu=edit_menu)

        # Создаем подменю "Помощь" #################################################
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="О программе", command=on_about_program)

        # Добавляем подменю "Помощь" к основному меню
        menu_bar.add_cascade(label="Помощь", menu=help_menu)

        # Устанавливаем основное меню для главного окна
        root.config(menu=menu_bar)

        # Создаем виджет вкладок ###################################################
        notebook = ttk.Notebook(root)

        ############################################################################
        # Вкладка 1
        t1 = TestMachine(window=root, notebook=notebook, russ_dict=russ_words, chin_dict=chin_words)

        ############################################################################
        # Вкладка 2
        t2 = BrainMachine(window=root, notebook=notebook, russ_dict=russ_words, chin_dict=chin_words)

        ############################################################################
        # Вкладка 3

        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text=' Адаптивный ')

        frame_base3 = tk.Frame(tab3)
        frame_base3.pack(expand=1, fill='both')

        ############################################################################

        notebook.pack(expand=1, fill='both')
        root.bind('<space>', space_event)

        on_diapason_words()

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
    
        file_content = read_file(file_path)
        self.russ_words, self.chin_words = parse_dictonary(file_content)

        self.t1.set_dicts(russ_dict=russ_words, chin_dict=chin_words)
        self.t2.set_dicts(russ_dict=russ_words, chin_dict=chin_words)



    def on_diapason_words():
        diap_window = WindowDiapasone(root=root)


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
 
 Текущая версия программы {VERSION}
 
 Программа абсолютно бесплатна ;-)



 Адрес для связи по любым ВАЖНЫМ вопросам:
 email: deciptikon@mail.ru
 
 """)
    
        self.label.pack(padx=20, pady=20)
        # Устанавливаем родительское окно для модального окна
        self.modal_window.transient(self.root)
        # Ожидаем закрытия модального окна перед возвращением к основному окну
        self.modal_window.wait_window(self.modal_window)

    def parse_dictonary(file_dictonary: str) -> [list[str], list[str]]:
        russ: list[str] = []
        chin: list[str] = []
        for line in file_dictonary.split('\n'):
            if len(line.strip()) > 0:
                c,r = line.split(' : ')
                russ.append(cut_str(long_str=r, max_len=50, slice_symbol=','))
                chin.append(c)
        return russ, chin
    
    # Действие при нажатии на Space
    def space_event(self, event):
        print('SPACE -->')
        index_tab = self.notebook.index(notebook.select())
        match index_tab:
            case 0:
                self.t1.on_button_next()
            case 1:
                if not self.t2.first_step:
                    self.t2.on_button_next()
            case 2:
                pass




# генерируем несколько различных целых чисел
def generate_random_indexes(min: int = 0, max: int = 7, num: int = 4) -> list[int]:
    return random.sample(range(min, max + 1), num)

# Сокращает строку до ближайшего символа slice_symbol с конца, 
# причём длина строки не будет превышать max_len
def cut_str(long_str: str = '', max_len: int = 50, slice_symbol: str = ','):
    slices_str = long_str.split(slice_symbol)
    short_str = ''
    for s in slices_str:
        if len(short_str + s) < max_len:
            short_str += s + slice_symbol
        else:
            break
    return short_str[:len(short_str)-1]

# Открытие файла
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Файл не найден"
    except Exception as e:
        return f"Ошибка чтения файла: {e}"





################################################################################
############  Тело GUI  ########################################################
################################################################################


root = tk.Tk()

root.mainloop()