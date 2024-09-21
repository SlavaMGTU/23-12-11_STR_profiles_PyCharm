#1.4	Сделана на базе плотли в 2024-06-16_app_exe.py
#D:\work\23-12-11_STR_profiles_PyCharm\2024-06-16_app_exe.py

import pandas as pd

import numpy as np

def det_of_relation_1Horse_app( child_name_gl, df, num_loc_gl):
    def search_for_parent(child_dic, parent_dic):
        # работа по словарям- Локус Исслед-Лошади(ребенка); Локус "с кем сравниваем"(родитель)
        # Итерируемся по строкам и перечисляем значения ячеек столбцов 'A' и 'B'
        # словарь локуса ребенка
        # словарь локуса родителя
        parent_point = 0  # совпадение локусов
        dif_no_ful_loc_point = 0  # кол-во несовпавших неполн локусов
        no_data_loc_point = 0  # кол-во локусов без даты
        char_count_df = 0 # кол-во букв в локусе

        for child_let in child_dic.values():
            if child_let != '' and child_let in parent_dic.values():  # буква Локуса ребенка совпадает
                parent_point = 1  # индекс состояния сравнения

        if '' in parent_dic.values():# в Локусе есть ''
            if  all(value == '' for value in parent_dic.values()):# в локусе обе буквы ==""
                no_data_loc_point = 1
            else:
                dif_no_ful_loc_point = 1
        for child_let in parent_dic.values():# считаю буквы локуса
            if child_let != '':
                char_count_df += 1

        return int(parent_point) , int(dif_no_ful_loc_point)  , int(no_data_loc_point) , int(char_count_df)

    relativ_data = {'ID': [],
                    'Кличка': [],
                    'Локусов совпало': [],
                    'Число лок. с 1 буквой': [],
                    'Локусы с 1 буквой': [],
                    'Число пустых лок.': [],
                    'Пустые локусы': [],
                    'Букв в профиле': [],
                    }

    df_relativ = pd.DataFrame(relativ_data)

    # Добавление новой колонки "id_f" из "ID Chromosoft" и "кличка"
    id_f_values = []
    for index, row in df.iterrows():
        value_id = row['ID Chromosoft']
        if pd.isna(value_id):
            value_id = ''
        elif type(value_id) is str:
            value_id = str(value_id)
        else:
            value_id = int(value_id)
        id_f_name = f"{value_id}_{row['кличка']}"
        if id_f_name in id_f_values:  # Если  элементe в столбце id_f  равен другой элемент из этого столбца -  ему присваивается номер
            id_f_name = id_f_name + f"_{id_f_values.count(id_f_name) + 1}"
        id_f_values.append(id_f_name)
    df['id_f'] = id_f_values

    rows_read = 0  # строка прочтения dataFrame

    child_name = df.at[df[df['кличка'] == child_name_gl].index[0], 'id_f']
    child_row_gl = df[df['id_f'] == child_name].index[0]

    for parent_name in df['id_f']:  # проход по всем строкам dataFrame

        progress = (rows_read / len(df)) * 100  # Расчет процента завершения
        rows_read += 1
        print(f"Прогресс: {progress:.2f}%")

        parent_index_gl = 0  # итоговое кол-во совпадений Локусов строки отчета

        dif_no_ful_loc_point_gl = 0
        dif_no_ful_loc_name_gl = ''
        no_data_loc_point_gl = 0
        no_data_loc_name_gl = ''
        char_count = 0 #  количество букв в пофиле (БВП)


        parent_gl = df[df['id_f'] == parent_name].index[0]

        # Инициализируем словари child_value и parent_value
        child_dic = {}
        parent_dic = {}
        #parent_point, no_data_loc_point, dif_no_ful_loc_point = 0, 0, 0 #НЕ ИСПОЛЬЗУЮ????!!!

        for numb_col_gl in range(2, 36, 2):
            # проходим по 2м буквам текущего сравниваемого локуса ребенка
            # Записываем данные из ячеек DataFrame в словарь child_value
            child_dic['A'] = df.at[child_row_gl, df.columns[numb_col_gl]]
            child_dic['B'] = df.at[child_row_gl, df.columns[numb_col_gl+1]]

            # Записываем данные из ячеек DataFrame в словарь parent_value
            parent_dic['A'] = df.at[parent_gl, df.columns[numb_col_gl]]
            parent_dic['B'] = df.at[parent_gl, df.columns[numb_col_gl + 1]]

            # Нахождение и замена значений float('nan') на string('')
            for dic in [child_dic, parent_dic]:
                for key, value in dic.items():
                    if isinstance(value, float) and np.isnan(value):
                        dic[key] = ''

            parent_point_new  , dif_no_ful_loc_point_new , no_data_loc_point_new, char_count_new = search_for_parent(child_dic, parent_dic)

            parent_index_gl += parent_point_new  # добавляем кол-во совпавших локусов
            char_count += char_count_new # добавляем кол-во букв

            if dif_no_ful_loc_point_new == 1:
                dif_no_ful_loc_point_gl += dif_no_ful_loc_point_new
                dif_no_ful_loc_name_gl += f'{df.columns[numb_col_gl][:-2]}, '

            if no_data_loc_point_new == 1:
                no_data_loc_point_gl += no_data_loc_point_new
                no_data_loc_name_gl += f'{df.columns[numb_col_gl][:-2]}, '

        if parent_index_gl >= num_loc_gl:

            parent_id = df['ID Chromosoft'].iloc[parent_gl]
            if pd.isna(parent_id):
                parent_id = ''
            elif type(parent_id) is str:
                parent_id = str(parent_id)
            else:
                parent_id = int(parent_id)

            parent_name_fin = df['кличка'].iloc[parent_gl]

            df_relativ.loc[len(df_relativ.index)] = [parent_id, parent_name_fin, parent_index_gl,
                                                     dif_no_ful_loc_point_gl, dif_no_ful_loc_name_gl,
                                                     no_data_loc_point_gl, no_data_loc_name_gl, char_count,
                                                     ]
            print(
                f"У Лошади: {child_name} совпадений {parent_index_gl}/17 с {parent_name}  //"
                f" неполн. проф. кол. {dif_no_ful_loc_point_gl} Локус: {dif_no_ful_loc_name_gl};//"
                f"НЕТ данных {no_data_loc_point_gl} Локус: {no_data_loc_name_gl};"
                f" Букв в проф {char_count}"
                )

    df_relativ = df_relativ.sort_values(by=['Локусов совпало'], ascending=False)

    return (df_relativ)