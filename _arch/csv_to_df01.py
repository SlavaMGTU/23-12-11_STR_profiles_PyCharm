# код обрабатывает переменное количество столбцов типа CSV в формат вставки датафрейма в код Есть текст:
# text = """
# 'название-столбец1','название-столбец2','название-столбец3','название-столбец4'
# 'ячейка1-столбца1','ячейка1-столбца2','ячейка1-столбца3','ячейка1-столбца4'
# ...
# """
# в следующий текст:
# "
# data = {'название-столбец1': ['ячейка1-столбца1', 'ячейка2-столбца1', 'ячейка3-столбца1', 'ячейка4-столбца1'],)
#         'название-столбец2': ['ячейка1-столбца2', 'ячейка2-столбца2', 'ячейка3-столбца2', 'ячейка4-столбца2'],...
# df = pd.DataFrame(data)

import pandas as pd

text = """
'id','кличка','age'
1,'Барсик',5
2,'Мурзик',4
3,'Рыжик',3
4,'Рыжик2',2
"""

# Split text into lines and extract column names
lines = text.strip().split('\n')
col_names = lines[0].replace("'", "").split(',')

# Create dictionary to store data
data = {col: [] for col in col_names}

# Extract values for each column
for line in lines[1:]:
    values = line.replace("'", "").split(',')
    for i, col_value in enumerate(values):
        data[col_names[i]].append(col_value)

# Create DataFrame
df = pd.DataFrame(data)

print("data = " + str(data))
print("df = pd.DataFrame(data)")
