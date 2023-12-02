import tkinter as tk

VERSION = '0.1.0'

def on_button_click():
    print("Кнопка была нажата!")

# Создаем главное окно
root = tk.Tk()
root.title("Chiness Trainer" + VERSION)

font_big = ("Arial", 56)  
font_small = ("Arial", 18)  

# Задаем размеры окна (ширина x высота + X + Y)
root.geometry("1000x600+200+100")

label_text = tk.Label(root, text="Текст 著名", font=font_big)
label_text.pack(pady=20)


# Создаем кнопку и привязываем к ней функцию on_button_click
button = tk.Button(root, text="Кнопка 著名", command=on_button_click, font=font_small)
button.pack(side="top", padx=100, pady=100)  # Пример настройки положения кнопки


# Запускаем цикл обработки событий
root.mainloop()