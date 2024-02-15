# продолжение файла 24-02-04_show_dFrame_3_data02 добавить в веб-приложение Dash кнопку "Определить_родство" при нажатие на которую запускается :
# def search_for_parents_all(child_row, parent1, parent2)
# ###
import dash
from dash import dcc, html
import pandas as pd
import base64
import io
import re

# Создание экземпляра приложения Dash
app = dash.Dash(__name__)

# Отображение меню выбора файла, выпадающих списков и кнопки "Определить_родство"
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    html.Div([
        html.Label('Ребенок'),  # Добавляем надпись "Ребенок" над выпадающим списком
        dcc.Dropdown(id='child-dropdown')
    ]),
    html.Div([
        html.Label('Родитель1'),  # Добавляем надпись "Родитель1" над выпадающим списком
        dcc.Dropdown(id='parent1-dropdown')
    ]),
    html.Div([
        html.Label('Родитель2'),  # Добавляем надпись "Родитель2" над выпадающим списком
        dcc.Dropdown(id='parent2-dropdown')
    ]),
    html.Button('Определить_родство', id='submit-button', n_clicks=0)  # Добавляем кнопку "Определить_родство"
])

# Функция для загрузки файла и считывания данных
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Если файл имеет расширение .csv, считываем его, используя pandas и модуль io
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8'))
            )
        else:
            return html.Div('Unsupported file format')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    unique_values = df['кличка'].unique()
    dropdown_options = [{'label': val, 'value': val} for val in unique_values]
    return dropdown_options

#доп.Функция для функц поиска родителей
def search_for_parents(df, child_row, parent1, parent2, numb_col):
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
                    case _:  # варианты 1/10
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


# Функция для поиска родителей
def search_for_parents_all(child_row_gl, parent1_gl, parent2_gl):# MARKBOOK!!!! ЗАКЛАДКА

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

    # данные по поиску
    #child_row_gl, parent1_gl, parent2_gl = 224, 220, 221  # 198
    # 130 Дионисия(дочь) 33 Догма(отец) 34Ибар РВ(мать)

    answ_fin = ''
    parent1_index_gl = 0
    parent2_index_gl = 0

    for numb_col_gl in range(2, 36, 2):
        answ = search_for_parents(child_row_gl, parent1_gl, parent2_gl, numb_col_gl)

        digits = re.findall(r'\d+', answ)

        match int(digits[-3]):
            case 1:
                if int(digits[-1]) == 1 or int(digits[-1]) == 10 or int(digits[-1]) == 11:
                    parent2_index_gl += 1
            case 2:
                if int(digits[-2]) == 1 or int(digits[-2]) == 10 or int(digits[-2]) == 11:
                    parent1_index_gl += 1
            case 4:
                if int(digits[-2]) != 0 and int(digits[-1]) != 0:
                    if int(digits[-2]) != int(digits[-1]):
                        parent1_index_gl += 1
                        parent2_index_gl += 1
                    elif int(digits[-2]) == 11:
                        parent1_index_gl += 1
                        parent2_index_gl += 1
                elif int(digits[-2]) != 0:
                    parent1_index_gl += 1
                elif int(digits[-1]) != 0:
                    parent2_index_gl += 1

        col_idx = int((numb_col_gl) / 2)
        df_result.loc[
            0, df_result.columns[col_idx]] = answ  # записать данные в датафрейм df_result под соответствующий столбец
        if 'Note' in answ or 'attention' in answ:
            answ_fin += df_result.columns[col_idx] + ': '
            answ_fin += answ

    if parent2_index_gl >= 16:
        answ_fin = f'родитель2 - ДА ({parent2_index_gl} из 17) ;' + answ_fin
    else:
        answ_fin = f'родитель2 - НЕТ ({parent2_index_gl} из 17) ;' + answ_fin

    if parent1_index_gl >= 16:
        answ_fin = f'родитель1 - ДА ({parent1_index_gl} из 17) ;' + answ_fin
    else:
        answ_fin = f'родитель1 - НЕТ ({parent1_index_gl} из 17) ;' + answ_fin

    return(answ_fin)
# Обратная связь для обновления выпадающих списков и запуска поиска родственных связей
@app.callback(
    [dash.dependencies.Output('child-dropdown', 'options'),
     dash.dependencies.Output('parent1-dropdown', 'options'),
     dash.dependencies.Output('parent2-dropdown', 'options')],
    [dash.dependencies.Input('upload-data', 'contents'),
     dash.dependencies.Input('upload-data', 'filename')]
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        options = parse_contents(list_of_contents, list_of_names)
        return options, options, options

# Обратная связь для обновления результатов по нажатию кнопки
@app.callback(
    dash.dependencies.Output('output-data-upload', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('child-dropdown', 'value'),
     dash.dependencies.State('parent1-dropdown', 'value'),
     dash.dependencies.State('parent2-dropdown', 'value')]
)
def update_result(df, n_clicks, child_value, parent1_value, parent2_value):
    if n_clicks > 0:
        # Вызов функции для поиска родителей
        result = search_for_parents_all(child_value, parent1_value, parent2_value)
        return result

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)