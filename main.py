import tkinter as tk
from tkinter import ttk
import random

VERSION = '0.2.2'

COLOR_GREEN = "#00AA55"
COLOR_RED   = "#AA2222"
COLOR_GRAY  = "#DDDDDD"

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
    global COLOR_GREEN 
    global COLOR_RED 

    global data_score_positive
    global data_score_negative
    global true_answer
    global first_step
    
    if button_number == true_answer:
        bt = buttons[button_number]
        bt.config(bg=COLOR_GREEN)
        if first_step:
            data_score_positive += 1
            label_score_positive1.config(text=f'+{data_score_positive}')
    else:
        bt = buttons[button_number]
        bt.config(bg=COLOR_RED)
        if first_step:
            data_score_negative += 1
            label_score_negative1.config(text=f' -{data_score_negative}')
    
    first_step = False

def on_button_next():
    global COLOR_GRAY

    global true_answer
    global first_step

    first_step = True

    indexes = generate_random_indexes(max=len(russ_words)-1)
    print(indexes)
    
    true_answer = random.randint(0, 3)
    print(true_answer)

    ind = indexes[true_answer]
    label_text1.config(text=chin_words[ind])

    i: int = 0
    for button in buttons:
        ind = indexes[i]
        button.config(text=russ_words[ind], bg=COLOR_GRAY)
        i += 1

def on_button_next2():
    global true_answer
    global first_step

    true_answer = random.randint(0, len(russ_words)-1)
    print(true_answer)
    first_step = True

    label_text2.config(text=chin_words[true_answer])
    text_input.delete(0, len(text_input.get()))

    button_check.config(bg=COLOR_GRAY)
    label_text_checker.config(text="Введите перевод по памяти.\n")



def on_button_check():
    global data_score_positive
    global data_score_negative
    global true_answer
    global first_step

    input_text_from_widget = text_input.get().split(',')
    

    true_words = russ_words[true_answer]

    for word in input_text_from_widget:
        #w = word.replace(' ','')
        w = word.strip()
        print(w)
        if len(w)>0 and w in true_words:
            if first_step:
                data_score_positive += 1
                first_step = False

                label_score_positive2.config(text=f'+{data_score_positive}')
                button_check.config(bg=COLOR_GREEN)

                label_text_checker.config(text=f'ВЕРНО!!!\n\"{true_words}\"')
                break
    if first_step:
        data_score_negative += 1
        first_step = False
        label_score_negative2.config(text=f'-{data_score_negative}')
        button_check.config(bg=COLOR_RED)
        label_text_checker.config(text=f'ОШИБКА, должно быть:\n\"{true_words}\"')



            

def space_event(event):
    match notebook.index(notebook.select()):
        case 0:
            button_next1.invoke()
        case 1:
            if not first_step:
                button_next2.invoke()
        case 2:
            pass
        

def enter_event(event):
    match notebook.index(notebook.select()):
        case 0:
            pass
        case 1:
            if first_step:
                button_check.invoke()
            else:
                button_next2.invoke()
            print('ENTER')
        case 2:
            pass

def num_event1(event):
    match notebook.index(notebook.select()):
        case 0:
            i = int(event.keysym) - 1
            buttons[i].invoke()
        case 1:
            pass
        case 2:
            pass

# Это не особо нужно и наверное я удалю это
def on_tab_changed(event):
    selected_tab = notebook.index(notebook.select())
    print(f"Активная вкладка: {selected_tab}")



file_content = read_file("Words.txt")
russ_words: list[str] = []
chin_words: list[str] = []
for line in file_content.split('\n'):
    if len(line) > 0:
        c,r = line.split(' : ')
        russ_words.append(cut_str(long_str=r, max_len=50, slice_symbol=','))
        chin_words.append(c)
        print(c + ' ---- ' + r)



root = tk.Tk()
root.title(f"Chiness Trainer {VERSION}")

font_big = ("Arial", 100)  
font_small = ("Arial", 18)  
font_score = ("Arial", 30)  

root.geometry("1000x600+400+200")


# Создаем виджет вкладок
notebook = ttk.Notebook(root)


############################################################################
# Вкладка 1

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text=' 4 варианта ')


label_text1 = tk.Label(tab1, text="[***]", font=font_big)
label_text1.pack(pady=10)

label_score_positive1 = tk.Label(tab1, text=f'+{data_score_positive}', font=font_score)
label_score_positive1.place(x = 10, y = 50)

label_score_negative1 = tk.Label(tab1, text=f' -{data_score_negative}', font=font_score)
label_score_negative1.place(x = 10, y = 100)


frame1 = tk.Frame(tab1)
frame1.pack(side=tk.TOP, pady=10)

buttons = []
for i in range(0, 4):
    button = tk.Button(frame1, text=f"****", 
                       command=lambda num=i: on_button_click(num), 
                       font=font_small, 
                       padx=10,
                       width=50)
    #button.pack(side=tk.LEFT, padx=10)
    button.grid(row=i, column=0, pady=10, padx=10 )
    root.bind(str(i+1), num_event1)
    buttons.append(button)


button_next1 = tk.Button(tab1, text=f"Next", 
                        command=lambda: on_button_next(), 
                        font=font_small, 
                        width=200, height=50,
                        bg='#DDDDDD')
button_next1.pack(side=tk.RIGHT, anchor=tk.SE)



############################################################################
# Вкладка 2

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text=' Письменный ')

frame2 = tk.Frame(tab2)
frame2.pack(side=tk.TOP, pady=10)

label_text2 = tk.Label(frame2, text="[***]", font=font_big)
label_text2.pack(pady=10)

label_score_positive2 = tk.Label(frame2, text=f'+{data_score_positive}', font=font_score)
label_score_positive2.place(x = 10, y = 50)

label_score_negative2 = tk.Label(frame2, text=f' -{data_score_negative}', font=font_score)
label_score_negative2.place(x = 10, y = 100)

text_input = tk.Entry(frame2, font=font_small, bg='#DDDDDD', width=200)
text_input.pack(pady=10, padx=100)

button_check = tk.Button(frame2, text=f"Check", 
                        command=lambda: on_button_check(), 
                        font=font_small, 
                        width=200, #height=50,
                        bg='#DDDDDD')
button_check.pack( pady=10, padx=50 )

label_text_checker = tk.Label(frame2, text="Введите перевод по памяти.\n", font=font_small)
label_text_checker.pack(pady=50)


button_next2 = tk.Button(tab2, text=f"Next", 
                        command=lambda: on_button_next2(), 
                        font=font_small, 
                        width=200, height=50,
                        bg='#DDDDDD')
button_next2.pack(side=tk.BOTTOM, anchor=tk.SE, pady=0)


############################################################################
# Вкладка 3

tab3 = ttk.Frame(notebook)
notebook.add(tab3, text=' Динамический ')

############################################################################

notebook.pack(expand=1, fill='both')
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

root.bind('<space>', space_event)
root.bind('<Return>', enter_event)

root.mainloop()