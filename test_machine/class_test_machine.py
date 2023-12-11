import tkinter as tk
from tkinter import ttk
from transitions import Machine
import random

from base_tab.class_base_tab import BaseTab
import constants

class TestMachine(BaseTab, object):
    true_answer: int = 0
    first_step: bool = True
    data_score_positive: int = 0
    data_score_negative: int = 0
    num_button = None

    def __init__(self, window, notebook, russ_dict: list[str], chin_dict: list[str], nameTab: str):
        super().__init__( window, notebook, russ_dict, chin_dict, nameTab)

        
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
        self.notebook.add(self.tab, text=self.nameTab)

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

        self.frame = tk.Frame(self.frame_base)
        self.frame.pack(side=tk.TOP, pady=10)

        self.buttons = []
        for i in range(1, 5):
            self.button = tk.Button(self.frame, text=f"****", 
                                command=lambda num=i-1: self.on_button_click(num), 
                                font=constants.FONT_SMALL, 
                                padx=10,
                                width=50)
            self.button.grid(row=i-1, column=0, pady=10, padx=10 )
            self.buttons.append(self.button)

        self.button_next = tk.Button(self.tab, text=f"Next", 
                                command=lambda: self.on_button_next(), 
                                font=constants.FONT_SMALL, 
                                width=200, height=50,
                                bg='#DDDDDD')
        self.button_next.pack(side=tk.RIGHT, anchor=tk.SE)
        self.next()

    # генерируем несколько различных целых чисел
    def generate_random_indexes(self, min: int = 0, max: int = 7, num: int = 4) -> list[int]:
        return random.sample(range(min, max + 1), num)

    def on_enter_Basic(self):
        print("State = Basic")
        self.num_button = None
        self.first_step = True
        indexes = self.generate_random_indexes(max=len(self.russ_words)-1)
        print(indexes)
        self.true_answer = random.randint(0, 3)
        print(self.true_answer)
        ind = indexes[self.true_answer]
        self.label_text.config(text=self.chin_words[ind])
        i: int = 0
        for button in self.buttons:
            ind = indexes[i]
            button.config(text=self.russ_words[ind], bg=constants.COLOR_GRAY)
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
        bt.config(bg=constants.COLOR_GREEN)
        if self.first_step:
            self.data_score_positive += 1
            self.label_score_positive.config(text=f'+{self.data_score_positive}')
        self.first_step = False

    # Callback-метод, вызываемый при входе в состояние False_answer
    def on_enter_False_answer(self):
        print("State = False_answer")
        bt = self.buttons[self.num_button]
        bt.config(bg=constants.COLOR_RED)
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

