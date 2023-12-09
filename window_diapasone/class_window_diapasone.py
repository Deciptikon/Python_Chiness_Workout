import tkinter as tk
from tkinter import ttk, messagebox
import constants

class WindowDiapasone(object):
    def __init__(self, root, tab1, tab2, russ_dict, chin_dict) -> None:
        self.root = root
        self.t1 = tab1
        self.t2 = tab2    
        self.russ_words = russ_dict
        self.chin_words = chin_dict
        
        self.modal_window = tk.Toplevel(self.root)
        self.modal_window.title("Настройка диапазона")
        self.modal_window.geometry("300x300+650+200")

        self.frame_base = tk.Frame(self.modal_window)
        self.frame_base.pack(expand=1, fill='both')

        self.label_min = tk.Label(self.frame_base, text="Min", font=constants.FONT_SMALL)
        self.label_min.pack(pady=10)
        self.spin_value_min = tk.StringVar(value='0')
        self.spinbox_min = ttk.Spinbox(self.frame_base, 
                                       from_=0, to=len(self.russ_words)-1, 
                                       textvariable=self.spin_value_min)
        self.spinbox_min.pack()

        self.label_max = tk.Label(self.frame_base, text="Max", font=constants.FONT_SMALL)
        self.label_max.pack(pady=10)
        self.spin_value_max = tk.StringVar(value=f'{len(self.russ_words)-1}')
        self.spinbox_max = ttk.Spinbox(self.frame_base, 
                                       from_=0, to=len(self.russ_words)-1, 
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
            russ_cuting = self.russ_words[min_value:max_value+1]
            chin_cuting = self.chin_words[min_value:max_value+1]
            self.t1.set_dicts(russ_dict=russ_cuting, chin_dict=chin_cuting)
            self.t2.set_dicts(russ_dict=russ_cuting, chin_dict=chin_cuting)
            messagebox.showinfo("Успешно", f"Диапазон от {min_value} до {max_value} успешно установлен")
            self.modal_window.destroy()

