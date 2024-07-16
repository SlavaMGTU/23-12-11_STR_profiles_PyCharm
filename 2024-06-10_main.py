# Поиск родителей для ЗАДАННОГО ребенка
# строка 140 ЗАМЕНА Номера и Имени ребенка в поиске
# 53 Знаменосец
# 3131 Гастроль (по-моему, она под кличкой Грань Твоей Души)
# 2402 Гармония
# 3249 Ракита
# 3057 Ночка Звёздная
import pandas as pd
import re


def search_for_parent(child_dic, parent_dic):
    #работа по словарям- Локус Исслед-Лошади(ребенка); Локус "с кем сравнив"(родитель)
        # Итерируемся по строкам и перечисляем значения ячеек столбцов 'A' и 'B'
     #словарь локуса ребенка
     #словарь локуса родителя
    parent_point = 0  # совпадение локусов
    dif_no_ful_loc_point = 0  # кол-во несовпавших неполн локусов
    no_data_loc_point = 0  # кол-во локусов без даты

    for child_let in child_dic.values():
        # !!!!!!!!
        # for child_let in child_dic.values:
        #     TypeError: 'builtin_function_or_method'
        #     object is not iterable
        if child_let != '' and child_let in parent_dic.values():# буква Локуса ребенка совпадает
            parent_point = 1  # индекс состояния сравнения

    if parent_point != 1:
        if '' in child_dic.values() or '' in parent_dic.values():# в Локусе есть ''
            if  len(set(child_dic.values()))== '' or len(set(parent_dic.values()))== '':# у одного в локусе обе буквы ==""
                no_data_loc_point = 1
            else:
                dif_no_ful_loc_point = 1

    return int(parent_point) , int(dif_no_ful_loc_point)  , int(no_data_loc_point)


df = pd.read_csv('D:\\work\\23-12-11_STR_profiles_PyCharm\\gitignore\\Книга12345.csv'
                 , sep=';', encoding='utf-8')  # чтение файла

relativ_data = {'id': [],
                'child': [],
                'parent': [],
                'parent_point': [],
                'dif_no_ful_loc_point': [],
                'dif_no_ful_loc_name': [],
                'no_data_loc_point': [],
                'no_data_loc_name': [],
                }

df_relativ = pd.DataFrame(relativ_data)

# Добавление новой колонки "id_f" из "ID Chromosoft" и "кличка"
id_f_values = []
for index, row in df.iterrows():
    id_f_name = f"{row['ID Chromosoft']}_{row['кличка']}"
    if id_f_name in id_f_values:  # Если  элементe в столбце id_f  равен другой элемент из этого столбца -  ему присваивается номер
        id_f_name = id_f_name + f"_{id_f_values.count(id_f_name) + 1}"
    id_f_values.append(id_f_name)
df['id_f'] = id_f_values

rows_read = 0# строка прочтения dataFrame
# for child_name in df['id_f']:
child_name = '2150_Румянец ВНИИК'  # '2150_Румянец'#'2610_Танго РВ'#!!!! ВВОД Номера и Имени ЛОШАДИ в поиске

for parent_name in df['id_f']:# проход по всем строкам dataFrame

    progress = (rows_read / len(df)) * 100  # Расчет процента завершения
    rows_read += 1
    print(f"Прогресс: {progress:.2f}%")

    if child_name != parent_name: # обходим чтоб не сравнивать лошадь с самой собой
        answ_fin = ''#итоговая строка отчета
        parent_index_gl = 0#итоговое кол-во совпадений Локусов строки отчета
        dif_no_ful_loc_point_gl = 0
        dif_no_ful_loc_name_gl = ''
        no_data_loc_point_gl = 0
        no_data_loc_name_gl = ''

        child_row_gl = df[df['id_f'] == child_name].index[0]
        parent_gl = df[df['id_f'] == parent_name].index[0]

        # Инициализируем словари child_value и parent_value
        child_dic = {}
        parent_dic = {}
        parent_point, no_data_loc_point, dif_no_ful_loc_point = 0 , 0 , 0

        for numb_col_gl in range(2, 36, 2):
            # проходим по 2м буквам текущего сравниваемого локуса ребенка
            # Записываем данные из ячеек DataFrame в словарь child_value
            #child_dic['A'] = df.loc[df['id_f'] == child_name, df.columns[numb_col_gl]]
            child_dic['A'] = df.at[child_row_gl, df.columns[numb_col_gl]]
            child_dic['B'] = df.at[child_row_gl, df.columns[numb_col_gl+1]]

            # Записываем данные из ячеек DataFrame в словарь parent_value
            parent_dic['A'] = df.at[parent_gl, df.columns[numb_col_gl]]
            parent_dic['B'] = df.at[parent_gl, df.columns[numb_col_gl+1]]

            parent_point_new  , dif_no_ful_loc_point_new , no_data_loc_point_new = search_for_parent(child_dic, parent_dic)

            parent_index_gl += parent_point_new

            if dif_no_ful_loc_point_new == 1:
                dif_no_ful_loc_point_gl += dif_no_ful_loc_point_new
                dif_no_ful_loc_name_gl += f', {df.columns[numb_col_gl][:-2]}'

            if no_data_loc_point_gl == 1:
                no_data_loc_point_gl += no_data_loc_point_new
                no_data_loc_name_gl += f', {df.columns[numb_col_gl][:-2]}'

    index_relativ = 12 # вводим значение порога допустимого совпадения
    if parent_index_gl >= index_relativ:
            df_relativ.loc[len(df_relativ.index)] = ['', child_name, parent_name, parent_index_gl,
                                                     dif_no_ful_loc_point_gl , dif_no_ful_loc_name_gl ,
                                                     no_data_loc_point_gl, no_data_loc_name_gl,
                                                     ]
            print(
                f"У Лошади: {child_name} совпадений {parent_index_gl}/17 с {parent_name}  //"
                f" неполных несовпад. проф. {dif_no_ful_loc_point_gl} Локус: {dif_no_ful_loc_name_gl};//"
                f"НЕТ данных {no_data_loc_point_gl} Локус: {no_data_loc_name_gl};"
            )

df_relativ.to_csv('file1.csv')
