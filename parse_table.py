import pandas as pd

path_to_file = 'book1000.xlsx'

table_from_file = pd.read_excel(path_to_file)

true_symbols = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И',
                'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т',
                'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь',
                'Э', 'Ю', 'Я',
                'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и',
                'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
                'э', 'ю', 'я'}

print("Первые несколько строк таблицы:")
print(table_from_file.head())

print(len(table_from_file))

string = ''
for i in range(3, len(table_from_file)-1):#len(table_from_file)-1
    c = str(table_from_file.at[i, 'Unnamed: 2']).strip()
    r = str(table_from_file.at[i, 'Unnamed: 4']).strip()
    if any(map(r.__contains__, true_symbols)):
        string += c + ' : ' + r.replace(';',',') + '\n'

    
with open('chinese_dict.txt', 'w', encoding="utf-8") as file:
    file.write(string)







