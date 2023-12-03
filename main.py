import tkinter as tk
import random

VERSION = '0.1.3'

# счёт правильных ответов
data_score: int = 0

# скрытвй параметр, номер верного ответа
true_answer: int = 0

# скрытый параметр, первый ход, первое нажатие
first_step: bool = True


# генерируем несколько различных целых чисел
def generate_random_indexes(min: int = 0, max: int = 7, num: int = 4) -> list[int]:
    return random.sample(range(min, max + 1), num)



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
    color_green = "#00AA55"
    color_red = "#AA2222"

    global data_score
    global true_answer
    global first_step
    

    if button_number == true_answer:
        bt = buttons[button_number]
        bt.config(bg=color_green)
        if first_step:
            data_score += 1
            label_score.config(text=f'Score = {data_score}')
    else:
        bt = buttons[button_number]
        bt.config(bg=color_red)
    
    first_step = False

def on_button_next():
    print(F"NEXT -->")
    color_gray = "#999999"

    global true_answer
    global first_step

    first_step = True

    indexes = generate_random_indexes()
    print(indexes)
    
    true_answer = random.randint(0, 3)
    print(true_answer)

    ind = indexes[true_answer]
    label_text.config(text=chin_words[ind])

    i: int = 0
    for button in buttons:
        ind = indexes[i]
        button.config(text=russ_words[ind], bg=color_gray)
        i += 1






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

font_big = ("Arial", 100)  
font_small = ("Arial", 18)  


root.geometry("1000x600+200+100")

label_text = tk.Label(root, text="著名", font=font_big)
label_text.pack(pady=10)

label_score = tk.Label(root, text=f'Score = {data_score}', font=font_small)
label_score.place(x = 25, y = 50)

#button1 = tk.Button(root, text="Кнопка 1", command=on_button_click, font=font_small)
#button1.pack(side="top", padx=100, pady=100) 


frame = tk.Frame(root)
frame.pack(side=tk.TOP, pady=10)

buttons = []
for i in range(0, 4):
    button = tk.Button(frame, text=f"Кнопка {i}", command=lambda num=i: on_button_click(num), font=font_small, padx=200)
    #button.pack(side=tk.LEFT, padx=10)
    button.grid(row=i, column=0, pady=10, padx=10 )
    buttons.append(button)

button_next = tk.Button(root, text=f"Next", command=lambda: on_button_next(), font=font_small, width=200, height=100)
button_next.pack(side=tk.RIGHT, anchor=tk.SE, padx=0, pady=0)




root.mainloop()