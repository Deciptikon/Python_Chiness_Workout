import tkinter as tk

VERSION = '0.1.2'

data_score: int = 0

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Файл не найден"
    except Exception as e:
        return f"Ошибка чтения файла: {e}"

def on_button_click(button_number):
    print(F"Кнопка {button_number} была нажата!")

def on_button_next():
    print(F"NEXT -->")

file_content = read_file("Words.txt")
russ_words = []
chin_words = []
for line in file_content.split('\n'):
    if len(line) > 0:
        c,r = line.split(' : ')
        russ_words.append(r)
        chin_words.append(c)
        print(c + ' ---- ' + r)


root = tk.Tk()
root.title("Chiness Trainer " + VERSION)

font_big = ("Arial", 56)  
font_small = ("Arial", 18)  


root.geometry("1000x600+200+100")

label_text = tk.Label(root, text="Текст 著名", font=font_big)
label_text.pack(pady=50)

label_score = tk.Label(root, text=f'Score = {data_score}', font=font_small)
label_score.place(x = 25, y = 50)

#button1 = tk.Button(root, text="Кнопка 1", command=on_button_click, font=font_small)
#button1.pack(side="top", padx=100, pady=100) 


frame = tk.Frame(root)
frame.pack(side=tk.TOP, pady=50)

for i in range(1, 5):
    button = tk.Button(frame, text=f"Кнопка {i}", command=lambda num=i: on_button_click(num), font=font_small, padx=200)
    #button.pack(side=tk.LEFT, padx=10)
    button.grid(row=i-1, column=0, pady=10, padx=10 )

button_next = tk.Button(root, text=f"Next", command=lambda: on_button_next(), font=font_small, width=200, height=100)
button_next.pack(side=tk.RIGHT, anchor=tk.SE, padx=0, pady=0)

width = root.winfo_width()
height = root.winfo_height()
print(f"Ширина окна: {width}, Высота окна: {height}")

root.mainloop()