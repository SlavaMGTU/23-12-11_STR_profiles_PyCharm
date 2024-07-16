import base64
import io
import webbrowser
from threading import Timer

#рабочая программа: PLOTLY+PyCHarm; скачивает данные из csv файла; выбирает лошадь вo всплывающем поле ; выбирает
# в поле количество совпадающих локусов; нажимает кнопку провести сравнение ; печатает интерактивную таблицу рез-тов
# Поиск родственников для ЗАДАННОй Лошади
#2024-06-16  версия 3.0(back-end) в plotly Работает , НО масштабирование таблицы; теперь надо доделать в  и  exe


import dash
from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table as dt

import dash_bootstrap_components as dbc

from determ_of_relation_1Horse_app03 import det_of_relation_1Horse_app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

table_data = {'ID': [],
                'Имя': [],
                'Локусов Совпало': [],
                'Кол-во Неполн Лок-ов': [],
                'Назв. Неполн Лок-ов': [],
                'Нет Лок-ов Кол-во': [],
                'Нет Лок-ов Имя': [],
                'Букв в Проф': [],
                }

df_table = pd.DataFrame(table_data)

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
    ),
    html.Div(id='output-data-upload'),# !!!!результат загрузки данных из файла

    html.Label('Сравниваемая'),
    dcc.Dropdown(
        id='child_dropdown',
        options=[],
        value=None,
        placeholder="Select Horse"
    ),

    html.Button('Определение родства у одной лошади', id='relation_button', n_clicks=0),  # Добавляем кнопку "Определение родства"

    dcc.Input(
        id="num_loc", type="number", value= 10,
        debounce=True, placeholder="Debounce True",
    ),

    html.Div(id='output'),  # Для вывода результата после нажатия кнопки
    html.Div(id='table_fin')  # Блок для отображения таблицы с датафреймом table_data
])

def open_browser():
	webbrowser.open_new("http://localhost:{}".format(8050))

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

@app.callback(
    Output('child_dropdown', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_child(contents, filename):
    if contents:
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        lst = [{'label': i, 'value': i} for i in df['кличка'].unique()]
        return lst
    else:
        return []

@app.callback(
    Output('table_fin', 'children'),  # Используем блок table_fin для отображения таблицы
    [Input('relation_button', 'n_clicks'),
     Input('upload-data', 'contents'),
     Input('upload-data', 'filename')],
    [State('child_dropdown', 'value'),
     State('num_loc', 'value')],
)
def update_output(n_clicks, contents, filename, child_value, num_loc):
    if n_clicks > 0:
        if contents is not None:
            df = parse_data(contents, filename)

            if df is None:
                return html.Div(['There was an error processing this file.'])
            else:
                df_table = det_of_relation_1Horse_app(child_value, df, num_loc)

                return dash_table.DataTable(
                    id='table',
                    columns=[{'name': i, 'id': i} for i in df_table.columns],
                    data=df_table.to_dict('records'),
                    sort_action='native',  # Разрешение на сортировку в браузере

                    style_table = {
                        'overflowX': 'auto',  # Добавить горизонтальную прокрутку для таблицы
                        'overflowY': 'auto',
                        'height': '400px',
                        'width': '100%',
                        'margin-left': 'auto',
                        'margin-right': 'auto',
                    },
                    style_cell = {
                        'textAlign': 'left',
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    },
                    style_header = {
                        'textAlign': 'left',
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    },



                # style_data = {
                #     'color': 'black',
                #     'backgroundColor': 'white'
                # },
                # style_data_conditional = [
                #     {
                #         'if': {'row_index': 'odd'},
                #         'backgroundColor': 'rgb(220, 220, 220)',
                #     }
                # ],
                # style_header = {
                #     'backgroundColor': 'rgb(210, 210, 210)',
                #     'color': 'black',
                #     'fontWeight': 'bold'
                # }

                )

    else:
        return ''


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=True, port=8050)
#pyinstaller --onedir 2024-06-12_app_exe.py
# cd /D D:\work\23-12-11_STR_profiles_PyCharm\dist\2024-05-13exe\2024-05-13exe.exe
#2024-05-13exe.exe
