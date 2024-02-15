import pandas as pd
# Создаем датафрейм
data = {'id': [1, 2, 3, 4],
        'кличка': ['Барсик', 'Мурзик', 'Рыжик', 'Рыжик2']}
df = pd.DataFrame(data)

chubziki = []

for i in range(len(df)):
    for j in range(len(df)):
        if i != j:
            for k in range(len(df)):
                if k != j and k != i:
                    if str(df[i] + df[min(j, k)] + df[max(j, k)]) not in chubziki:
                        chubziki.append(str(df[i] + df[min(j, k)] + df[max(j, k)]))

print(chubziki, sep = '\n')