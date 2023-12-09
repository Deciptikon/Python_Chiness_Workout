import tkinter as tk
from tkinter import ttk
from transitions import Machine
import random

from base_tab.class_base_tab import BaseTab
import constants

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

        self.label_text = tk.Label(self.frame_base, 
                                   text="[***]", 
                                   font=constants.FONT_BIG)
        self.label_text.pack(pady=10)

        self.label_score_positive = tk.Label(self.frame_base, 
                                             text=f'+{self.data_score_positive}', 
                                             font=constants.FONT_SCORE)
        self.label_score_positive.place(x = 10, y = 50)

        self.label_score_negative = tk.Label(self.frame_base, 
                                             text=f' -{self.data_score_negative}', 
                                             font=constants.FONT_SCORE)
        self.label_score_negative.place(x = 10, y = 100)

        self.text_input = tk.Entry(self.frame_base, font=constants.FONT_SMALL, bg='#DDDDDD', width=200)
        self.text_input.pack(pady=10, padx=100)

        self.button_check = tk.Button(self.frame_base, text=f"Check", 
                                command=lambda: self.on_button_check(), 
                                font=constants.FONT_SMALL, 
                                width=200, #height=50,
                                bg='#DDDDDD')
        self.button_check.pack( pady=10, padx=50 )

        self.label_text_checker = tk.Label(self.frame_base, 
                                           text="Введите перевод по памяти.\n", 
                                           font=constants.FONT_SMALL)
        self.label_text_checker.pack(pady=50)

        self.button_next = tk.Button(self.tab, text=f"Next", 
                        command=lambda: self.on_button_next(), 
                        font=constants.FONT_SMALL, 
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
        self.button_check.config(bg=constants.COLOR_GRAY)
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
        self.button_check.config(bg=constants.COLOR_GREEN)
        self.label_text_checker.config(text=f'ВЕРНО!!!\n\"{self.true_words}\"')

    # Callback-метод, вызываемый при входе в состояние False_answer
    def on_enter_False_answer(self):
        print("State = False_answer")
        self.data_score_negative += 1
        self.first_step = False
        self.label_score_negative.config(text=f'-{self.data_score_negative}')
        self.button_check.config(bg=constants.COLOR_RED)
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
