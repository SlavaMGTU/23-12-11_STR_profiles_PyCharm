import pandas as pd


def search_for_parents(child_row, parent1, parent2):
    # # Создаем список строк родителей для итерации
    # parents_rows = [0, 1]
    # child_row = 2
    parents_rows = [parent1, parent2]
    # Итерируемся по строкам и перечисляем значения ячеек столбцов 'A' и 'B'
    # Получаем итоговые  коэф определяющ с каким разрядом/буквой совпадение у родителя
    parent1_index = 0
    parent2_index = 0
    child_index = -1
    null_index = 4  # индекс что все участники имеют не пустые значения
    for child_let in df.loc[df['id'] == child_row, ['A', 'B']]:
        child_value = df.loc[child_row, child_let]
        child_index += 1
        if child_value != '' and null_index != 0:  # текущ знач у ребенка не пустое и индекс не пустой
            parent_index = 0
            for row in parents_rows:
                parent_index += 1
                for col in ['A', 'B']:
                    parent_value = df.loc[row, col]
                    if parent_value != '' and null_index != parent_index and null_index != 3:  # текущ знач у родителя не пустое или
                        # не равен пустому индексу у текущего родителя или обоих родителей
                        if parent_value == child_value:  # локус родителя совпадает с потомком
                            if row == parents_rows[0]:  # строка родителя является первой
                                parent1_index += 1 * (10 ** child_index)  # если 1- совп с A у ребенка; 10 - совп с B у ребенка;
                                # print(f"Значение Child в строке {child_let}: {child_value}")
                                # print(f"Значение Родитель1 в строке {col}: {parent_value}")
                            else:
                                parent2_index += 1 * (10 ** child_index)
                                # print(f"Значение Child в строке {child_let}: {child_value}")
                                # print(f"Значение Родитель2 в строке {col}: {parent_value}")
                    else:
                        if parent_value == '':  # текущ знач у родителя пустое
                            if null_index == 4 or null_index == parent_index:  # до этого пустых не было или пустой был того-же родителя
                                null_index = parent_index
                            else:
                                null_index = 3
        else:
            null_index = 0

    # варианты 0/1/2/10/11/12/20/21/22
    # 0- нет совп/1 - перв букв Ребенк совп с род /2- перв букв Ребенк совп с 2мя букв род /
    # 10 - 2я букв Ребенк совп с род /11 - обе буквы Ребенк совп с род /20 - 2я букв Ребенк совп с 2мя род/
    # 21/22
    if parent1_index == 2:
        parent1_index = 1
    elif parent1_index == 20:
        parent1_index = 10
    elif parent1_index == 12 or parent1_index == 21 or parent1_index == 22:
        parent1_index = 11

    if parent2_index == 2:
        parent2_index = 1
    elif parent2_index == 20:
        parent2_index = 10
    elif parent2_index == 12 or parent2_index == 21 or parent2_index == 22:
        parent2_index = 11

    # print(f"Родитель1 совпадений: {parent1_index}")
    # print(f"Родитель2 совпадений: {parent2_index}")
    answ = ''  # результат функции
    match null_index:
        case 0:
            answ = answ + "Нет данных по ребенку attention; "
        case 1:
            answ = answ + "Нет данных по Родитель1 attention; "
            if parent2_index == 0:
                answ = answ + f"Родитель2 Note {parents_rows[1]} - НЕТ совпадений; "
            else:
                answ = answ + f"Родитель2 {parents_rows[1]} - ЕСТЬ совпадение/я; "
        case 2:
            answ = answ + "Нет данных по Родитель2 attention; "
            if parent1_index == 0:
                answ = answ + f"Родитель1 Note {parents_rows[0]} - НЕТ совпадений; "
            else:
                answ = answ + f"Родитель1 {parents_rows[0]} - ЕСТЬ совпадение/я; "
        case 3:
            answ = answ + "Нет данных по родителям attention; "
        case 4:
            answ = answ + "ЕСТЬ ВСЕ данные; "
            if parent1_index == parent2_index:
                match parent1_index:
                    case 0:
                        answ = answ + "Оба НЕ родители Note; "  # "Оба родителя не имеют буквы у потомка"
                    case 11:
                        answ = answ + "Оба могут быть родителями; "  # Оба родителя имеют ОБЕ буквы у потомка
                    case _:# варианты 1/2/10
                        answ = answ + "Неопределенность attention; "  # Вариант неопределённости; Оба родителя имеют по одной букве у потомка и эти буквы у родителей пересекаются
            else:
                if parent1_index == 0 or parent2_index == 0:
                    if parent1_index == 0:
                        answ = answ + f"Родитель1 Note {parents_rows[0]} - НЕТ совпадений; "
                        answ = answ + f"Родитель2 {parents_rows[1]} - ЕСТЬ совпадение/я; "
                    else:
                        answ = answ + f"Родитель1 {parents_rows[0]} - ЕСТЬ совпадение/я; "
                        answ = answ + f"Родитель2 Note {parents_rows[1]} - НЕТ совпадений; "
                else:
                    answ = answ + "Оба могут быть родителями; "
    return answ

# Создание датафрейма
data = {'id': [1, 2, 3, 4, 5, 6],
         'A': ['O', 'O', 'O', 'M', 'M', 'M' ],
         'B': ['O', 'O', 'O', 'O', 'J', 'O' ]}
df = pd.DataFrame(data)

# Вывод датафрейма
print(df)

answ = search_for_parents(2, 0, 1)
print(answ )