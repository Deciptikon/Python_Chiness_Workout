import tkinter as tk

def on_button_click():
    print("Кнопка была нажата!")

# Создаем главное окно
root = tk.Tk()
root.title("Пример с кнопкой")

# Задаем размеры окна (ширина x высота + X + Y)
root.geometry("400x300+100+100")

# Создаем кнопку и привязываем к ней функцию on_button_click
button = tk.Button(root, text="Нажми меня!", command=on_button_click)
#button.pack(pady=20)
button.pack(side="top", padx=10, pady=10)  # Пример настройки положения кнопки


# Запускаем цикл обработки событий
root.mainloop()