import pandas as pd
from datetime import datetime
import subprocess

# формат времени на русском
import locale

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

# распаковка zip папки
subprocess.run("unzip -o 786442_Ribbon1\ Сводная.zip", shell=True)

# читаем csv файл
df = pd.read_csv("786442_Ribbon1 Сводная.csv", sep=";", encoding="cp1251", decimal=",")

# конвертируем дату
df["Дата и время записи"] = pd.to_datetime(df["Дата и время записи"], format="%d %B %Y г. %H:%M:%S.%f мсек")


def select(datetime_start, datetime_end, apertura, df):
    df = df[(df["Дата и время записи"] > datetime_start) & (df["Дата и время записи"] <= datetime_end)]

    # если требуется сортировка таблицы по дате
    # df = df.sort_values(by="Дата и время записи")

    s = set()
    for column, dopusk in apertura.items():
        column_id = df.columns.get_loc(column)
        for i in range(1, df.shape[0]):
            if abs(df.iat[i, column_id] - df.iat[i - 1, column_id]) > dopusk:
                s.add(i)
    df = df.iloc[sorted(set(s))]
    return df


start_time = datetime.now()

df = select(
    datetime.strptime("2022-08-18 07:00:00.000", "%Y-%m-%d %H:%M:%S.%f"),  # время начала фильтра
    datetime.strptime("2022-08-18 09:00:00.000", "%Y-%m-%d %H:%M:%S.%f"),  # время конца фильтра
    {
        # номер параметра: максимальная погрешность отклонения(аппертура)
        "п11": 0.0001,
        "п12": 1,
    },
    df,
)

delta_time = datetime.now() - start_time
print("Время работы функции на поиск отклонений: ", delta_time)

df.to_csv(
    "result.csv", sep=";", encoding="cp1251", decimal=",", date_format="%d %B %Y г. %H:%M:%S.%f мсек", index=False
)
# print(df)
