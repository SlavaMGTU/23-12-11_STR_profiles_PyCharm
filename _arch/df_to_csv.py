import pandas as pd

data = {'id': [1, 2, 3, 4],
        'кличка': ['Барсик', 'Мурзик', 'Рыжик', 'Рыжик2']}
df = pd.DataFrame(data)

result = df.to_csv(index=False)
header = result[:result.index('\n')]
#print(header)
print(result)