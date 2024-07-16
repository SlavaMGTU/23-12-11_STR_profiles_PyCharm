import base64
import io
import webbrowser
from threading import Timer

import dash
from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table as dt

import dash_bootstrap_components as dbc

from determ_of_relation_1Horse_app02 import det_of_relation_1Horse_app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

table_data={'parent_name': [],
            'parent_index_gl': [],
            'dif_no_ful_loc_point_gl': [],
            'dif_no_ful_loc_name_gl': [],
            'no_data_loc_point_gl': [],
            'no_data_loc_name_gl': [],
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

    html.Label('Ребенок'),
    dcc.Dropdown(
        id='child_dropdown',
        options=[],
        value=None,
        placeholder="Select child"
    ),

    html.Label('Родитель1'),
    dcc.Dropdown(
        id='parent1_dropdown',
        options=[],
        value=None,
        placeholder="Select parent1"
    ),

    html.Label('Родитель2'),
    dcc.Dropdown(
        id='parent2_dropdown',
        options=[],
        value=None,
        placeholder="Select parent2",
    ),


    html.Button('Определение родства 1й лошади', id='relation_button', n_clicks=0),  # Добавляем кнопку "Определение родства"
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
    Output('parent1_dropdown', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_parent1(contents, filename):
    if contents:
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        lst = [{'label': i, 'value': i} for i in df['кличка'].unique()]
        return lst
    else:
        return []


@app.callback(
    Output('parent2_dropdown', 'options'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')])
def update_parent2(contents, filename):
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
    [State('child_dropdown', 'value')]
)
def update_output(n_clicks, contents, filename, child_value):
    if n_clicks > 0:
        if contents is not None:
            df = parse_data(contents, filename)

            if df is None:
                return html.Div(['There was an error processing this file.'])
            else:
                df_table = det_of_relation_1Horse_app(child_value, df)

                return dash_table.DataTable(
                    id='table',
                    columns=[{'name': i, 'id': i} for i in df_table.columns],
                    data=df_table.to_dict('records'),
                    sort_action='native',  # Разрешение на сортировку в браузере
                    style_table={'overflowX': 'auto'}  # Добавить горизонтальную прокрутку для таблицы
                )

    else:
        return ''

# @app.callback(
#     Output('output-data-upload', 'children'),
#     [Input('upload-data', 'contents')],
#     [State('upload-data', 'filename')]
# )
# def display_table(contents, filename):
#     if contents is not None:
#         df = parse_data(contents, filename)
#         return dash_table.DataTable(
#             id='table',
#             columns=[{'name': i, 'id': i} for i in df.columns],
#             data=df.to_dict('records'),
#         )


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=True, port=8050)
#pyinstaller --onedir 2024-06-12_app_exe.py
# cd /D D:\work\23-12-11_STR_profiles_PyCharm\dist\2024-05-13exe\2024-05-13exe.exe
#2024-05-13exe.exe
