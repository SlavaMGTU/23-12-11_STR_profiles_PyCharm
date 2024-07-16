import base64
import io
import webbrowser
from threading import Timer

import dash
from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
from dash.dependencies import Input, Output, State

from determ_of_relation_1Horse_app01 import det_of_relation_1Horse_app

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

    #Интерактивная таблица в : app.layout = html.Div([...
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df_table.columns],
        data=df_table.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Div(id='datatable-interactivity-container'),

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

#Интерактивная таблица
@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

#Интерактивная таблица
@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    # При первом отображении таблицы `derived_virtual_data` и `derived_virtual_selected_rows` будут `None`. Это связано
    # с особенностями в Dash (Непредоставленные свойства всегда  None и Dash вызывает зависимые обратные вызовы при
    # первой визуализации компонента). Поэтому если `rows` это  `None`, значит компонент был только что отображен, и
    # его значение будет таким же, как и в компоненте Датафрейма. Вместо установки здесь None вы также можете установить
    # 'derived_virtual_data=df.to_rows('dict')'` при инициализации компонента.

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df_table if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff['parent_name'],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # проверяем, существует ли столбец — возможно, пользователь удалил его. Если `column.deletable=False`, вам не
        # нужно выполнять эту проверку.

        for column in ["pop", "lifeExp", "gdpPercap"] if column in dff
    ]

@app.callback(
    Output('output', 'children'),
    [Input('relation_button', 'n_clicks'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')],
    [State('child_dropdown', 'value'),
    State('parent1_dropdown', 'value'),
    State('parent2_dropdown', 'value')]
)
def update_output(n_clicks, contents, filename, child_value, parent1_value, parent2_value):
    if n_clicks > 0:
        #answ = f'Selected values: Child - {child_value}, Parent1 - {parent1_value}, Parent2 - {parent2_value}'
        if contents is not None:
            df = parse_data(contents, filename)

            if df is None:
                return html.Div(['There was an error processing this file.'])
            else:
                df_table = f'ИТОГИ: {det_of_relation_1Horse_app(child_value, parent1_value, parent2_value, df)}'
                return df_table

    else:
        return ''


if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=True, port=8050)
#pyinstaller --onedir 2024-06-12_app_exe.py
# cd /D D:\work\23-12-11_STR_profiles_PyCharm\dist\2024-05-13exe\2024-05-13exe.exe
#2024-05-13exe.exe
