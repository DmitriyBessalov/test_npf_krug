import pandas as pd
import subprocess
from datetime import datetime

import locale

# формат даты на русском
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

# распаковка zip папки
subprocess.run("unzip -o 786442_Ribbon1\ Сводная.zip", shell=True)

# читаем csv файл
df = pd.read_csv("786442_Ribbon1 Сводная.csv", sep=";", encoding='cp1251', low_memory=False)

# index строки с максимальным значением
current_row = df['RecordID'].idxmax()

# Получим максимальное значение в столбце "RecordID"
RecordID_max = df.iloc[current_row]['RecordID']

# количество строк для обновления в таблице
max_row = df.shape[0] - 1
# количество колонок с параметрами
max_collumn = df.shape[1] - 2

# запускам цикл на добавление 10 сток
for i in range(10):

    # сброс цикла записи строк
    if max_row == current_row:
        current_row = 0

    # получаем id записи
    RecordID_max += 1

    # изменяем данные строки
    data = [RecordID_max, datetime.now().strftime("%d %B %Y г. %-H:%M:%S.%f")[:-3] + " мсек"]
    for i2 in range(max_collumn):
        data.append(i2+1)

    # Обновляем датафрейм
    df.loc[current_row] = data

    # получаем номер строки для обновления
    current_row += 1


def select_max_change_apertura(timestamp_start, timestamp_end, apertur):

    return df


start_time = datetime.now()

df = select_max_change_apertura(
    "7:57:53.002",  # время начала фильтра
    "8:57:53.002",  # время конца фильтка
    {
        4: 1,  # номер парамера и максимальное отклонение
        6: 1,
    })

end_time = datetime.now()
delta_time = end_time - start_time
print("Время работы функции на поиск отклонений: ", delta_time)


df.to_csv("786442_Ribbon1 Сводная.csv", sep=";", encoding="cp1251", date_format='%Y%m%d')
