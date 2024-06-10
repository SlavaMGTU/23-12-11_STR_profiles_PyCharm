# Поиск родственников для ЗАДАННОй лошади
# строка 140 ЗАМЕНА Номера и Имени ребенка в поиске
#53 Знаменосец
#3131 Гастроль (по-моему, она под кличкой Грань Твоей Души)
#2402 Гармония
#3249 Ракита
#3057 Ночка Звёздная
import pandas as pd
import re

def search_for_parents(child_row, parent1, parent2, numb_col):
    parents_rows = [parent1, parent2]
    # Итерируемся по строкам и перечисляем значения ячеек столбцов 'A' и 'B'
    # Получаем итоговые  коэф определяющ с каким разрядом/буквой совпадение у родителя
    parent1_index = 0
    parent2_index = 0
    child_index = -1
    null_index = 4  # индекс что все участники имеют не пустые значения
    for child_let in df.loc[df['ID Chromosoft'] == child_row, [df.columns[numb_col], df.columns[numb_col + 1]]]:
        child_value = df.loc[child_row, child_let]
        child_index += 1
        if child_value != '' and null_index != 0:  # текущ знач у ребенка не пустое и индекс не пустой
            parent_index = 0
            for row in parents_rows:
                parent_index += 1
                for col in [df.columns[numb_col], df.columns[numb_col + 1]]:
                    parent_value = df.loc[row, col]
                    if parent_value != '' and null_index != parent_index and null_index != 3:  # текущ знач у родителя не пустое или
                        # не равен пустому индексу у текущего родителя или обоих родителей
                        if parent_value == child_value:  # локус родителя совпадает с потомком
                            if row == parents_rows[0]:  # строка родителя является первой
                                parent1_index += 1 * (
                                            10 ** child_index)  # если 1- совп с A у ребенка; 10 - совп с B у ребенка;
                            else:
                                parent2_index += 1 * (10 ** child_index)
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
    answ = answ + f" {null_index} {'{:02d}'.format(parent1_index)} {'{:02d}'.format(parent2_index)} ; "
    return answ
df = pd.read_csv('D:\\work\\23-12-11_STR_profiles_PyCharm\\gitignore\\Книга123.csv'
    ,sep=';', encoding='utf-8')#чтение файла

resalt = {'id': [0],
        'VHL20_FAM': [''],
        'HTG4_FAM': [''],
        'AHT4_FAM': [''],
        'HMS7_FAM': [''],
        'HTG6_VIC': [''],
        'AHT5_VIC': [''],
        'HMS6_VIC': [''],
        'ASB23_VIC': [''],
        'ASB2_VIC': [''],
        'HTG10_NED': [''],
        'HTG7_NED': [''],
        'HMS3_NED': [''],
        'HMS2_NED': [''],
        'ASB17_PET': [''],
        'LEX3_PET': [''],
        'HMS1_PET': [''],
        'CA425_PET': [''],
        }
df_result = pd.DataFrame(resalt)

relativ_data = {'id': [],
                'child': [],
                'parent1': [],
                'parent2': [],
                'parent1_points': [],
                'parent2_points': [],
                }
df_relativ = pd.DataFrame(relativ_data)

# Добавление новой колонки "id_f" из "ID Chromosoft" и "кличка"
id_f_values = []
for index, row in df.iterrows():
    id_f = f"{row['ID Chromosoft']}_{row['кличка']}"
    if id_f in id_f_values:#Если  элементe в столбце id_f  равен другой элемент из этого столбца -  ему присваивается номер
        id_f = id_f + f"_{id_f_values.count(id_f) + 1}"
    id_f_values.append(id_f)
df['id_f'] = id_f_values

rows_read = 0
#for child in df['id_f']:
child ='3057_Ночка Звездная РВ'#'2150_Румянец'#'2610_Танго РВ'#!!!! ЗАМЕНА Номера и Имени ребенка в поиске

for parent1 in df['id_f']:

    num_rows = len(df)
    progress = (rows_read / len(df)) * 100  # Расчет процента завершения
    rows_read += 1
    print(f"Прогресс: {progress:.2f}%")

    for parent2 in df['id_f']:
        if child != parent1 and child != parent2:
            if  parent1 != parent2:
                answ_fin = ''
                parent1_index_gl= 0
                parent2_index_gl= 0
                child_row_gl = df[df['id_f'] == child].index[0]
                parent1_gl = df[df['id_f'] == parent1].index[0]
                parent2_gl = df[df['id_f'] == parent2].index[0]

                for numb_col_gl in range(2,36,2):
                    answ = search_for_parents(child_row_gl, parent1_gl, parent2_gl, numb_col_gl)

                    digits = re.findall(r'\d+', answ)

                    match int(digits[-3]):
                        case 1:
                            if  int(digits[-1]) == 1 or int(digits[-1]) ==10 or int(digits[-1]) ==11:
                                parent2_index_gl += 1
                        case 2:
                            if  int(digits[-2]) == 1 or int(digits[-2]) ==10 or int(digits[-2]) ==11:
                                parent1_index_gl += 1
                        case 4:
                            if int(digits[-2]) != 0 and int(digits[-1]) != 0:
                                if int(digits[-2]) !=  int(digits[-1]):
                                    parent1_index_gl += 1
                                    parent2_index_gl += 1
                                elif int(digits[-2]) == 11:
                                    parent1_index_gl += 1
                                    parent2_index_gl += 1
                            elif int(digits[-2]) != 0:
                                parent1_index_gl += 1
                            elif  int(digits[-1]) != 0:
                                parent2_index_gl += 1

                    col_idx = int((numb_col_gl) / 2)
                    df_result.loc[0, df_result.columns[col_idx]] = answ #записать данные в датафрейм df_result под соответствующий столбец
                    if 'Note' in answ or 'attention' in answ:
                        answ_fin += df_result.columns[col_idx]+': '
                        answ_fin += answ

                if  parent1_index_gl >= 12 and parent2_index_gl >= 12 :
                    df_relativ.loc[len(df_relativ.index)] = ['', child , parent1, parent2, parent1_index_gl, parent2_index_gl]
                    print(f"Ребенок: {child}; Род1:{parent1} {parent1_index_gl}/17 ; Род2:{parent2} {parent2_index_gl}/17 ;")


df_relativ.to_csv('file1.csv')