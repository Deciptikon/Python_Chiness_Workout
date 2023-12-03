import tkinter as tk
import random

VERSION = '0.1.5'

# счёт правильных ответов
data_score_positive: int = 0

# счёт НЕправильных ответов
data_score_negative: int = 0

# скрытвй параметр, номер верного ответа
true_answer: int = 0

# скрытый параметр, первый ход, первое нажатие
first_step: bool = True


# генерируем несколько различных целых чисел
def generate_random_indexes(min: int = 0, max: int = 7, num: int = 4) -> list[int]:
    return random.sample(range(min, max + 1), num)

def cut_str(long_str: str = '', max_len: int = 50, slice_symbol: str = ','):
    slices_str = long_str.split(slice_symbol)
    short_str = ''
    for s in slices_str:
        if len(short_str + s) < max_len:
            short_str += s + slice_symbol
        else:
            break
    return short_str[:len(short_str)-1]


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
    color_green = "#00AA55"
    color_red = "#AA2222"

    global data_score_positive
    global data_score_negative
    global true_answer
    global first_step
    

    if button_number == true_answer:
        bt = buttons[button_number]
        bt.config(bg=color_green)
        if first_step:
            data_score_positive += 1
            label_score_positive.config(text=f'+{data_score_positive}')
    else:
        bt = buttons[button_number]
        bt.config(bg=color_red)
        if first_step:
            data_score_negative += 1
            label_score_negative.config(text=f' -{data_score_negative}')
    
    first_step = False

def on_button_next():
    color_gray = "#DDDDDD"

    global true_answer
    global first_step

    first_step = True

    indexes = generate_random_indexes(max=len(russ_words)-1)
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

def space_event(event):
    button_next.invoke()

def num_event(event):
    i = int(event.keysym) - 1
    buttons[i].invoke()



file_content = read_file("Words.txt")
russ_words = []
chin_words = []
for line in file_content.split('\n'):
    if len(line) > 0:
        c,r = line.split(' : ')
        russ_words.append(cut_str(long_str=r, max_len=50, slice_symbol=','))
        chin_words.append(c)
        print(c + ' ---- ' + r)


root = tk.Tk()
root.title("Chiness Trainer " + VERSION)

font_big = ("Arial", 100)  
font_small = ("Arial", 18)  
font_score = ("Arial", 30)  

root.geometry("1000x600+400+200")

label_text = tk.Label(root, text="[***]", font=font_big)
label_text.pack(pady=10)

label_score_positive = tk.Label(root, text=f'+{data_score_positive}', font=font_score)
label_score_positive.place(x = 10, y = 50)

label_score_negative = tk.Label(root, text=f' -{data_score_negative}', font=font_score)
label_score_negative.place(x = 10, y = 100)


frame = tk.Frame(root)
frame.pack(side=tk.TOP, pady=10)

buttons = []
for i in range(0, 4):
    button = tk.Button(frame, text=f"****", 
                       command=lambda num=i: on_button_click(num), 
                       font=font_small, 
                       padx=10,
                       width=50)
    #button.pack(side=tk.LEFT, padx=10)
    button.grid(row=i, column=0, pady=10, padx=10 )
    root.bind(str(i+1), num_event)
    buttons.append(button)


button_next = tk.Button(root, text=f"Next", 
                        command=lambda: on_button_next(), 
                        font=font_small, 
                        width=200, height=50,
                        bg='#DDDDDD')
button_next.pack(side=tk.RIGHT, anchor=tk.SE)
root.bind('<space>', space_event)


root.mainloop()