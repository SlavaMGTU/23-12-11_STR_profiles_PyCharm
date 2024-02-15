import pandas as pd
from io import StringIO

text = """
'id','кличка','age','extra'
1,'Барсик',5,9
2,'Мурзик',4,10
3,'Рыжик',3,11
4,'Рыжик2',2,12
"""

# Преобразуем текст в удобный для pandas формат
data = StringIO(text)

# Чтение данных в DataFrame
df = pd.read_csv(data, sep=',', quotechar="'")

# Преобразование DataFrame в словарь, где ключи - названия столбцов, значения - списки значений
data = df.to_dict(orient='list')

# Создание нового DataFrame из словаря
df = pd.DataFrame(data)

print(df)