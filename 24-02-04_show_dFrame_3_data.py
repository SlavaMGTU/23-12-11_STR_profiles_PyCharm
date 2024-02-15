# продолжение файла 24-02-03_read-csv_show-table00.py Для отображения уникальных значений столбца 'кличка' из DataFrame в выпадающем списке в веб-приложении Dash
import dash
from dash import dcc, html
import pandas as pd
import base64
import io

# Создание экземпляра приложения Dash
app = dash.Dash(__name__)

# Отображение меню выбора файла и выпадающего списка
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
        dcc.Dropdown(id='column-dropdown')
    ])
])

# Функция для загрузки файла и считывания данных
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Если файл имеет расширение .csv, считываем его, используя pandas и модуль io
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            return html.Div('Unsupported file format')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    unique_values = df['кличка'].unique()
    dropdown_options = [{'label': val, 'value': val} for val in unique_values]
    return dcc.Dropdown(
        id='column-dropdown',
        options=dropdown_options,
        value=dropdown_options[0]['value']
    )

# Обратная связь для обновления выпадающего списка
@app.callback(
    dash.dependencies.Output('output-data-upload', 'children'),
    [dash.dependencies.Input('upload-data', 'contents'),
     dash.dependencies.Input('upload-data', 'filename')])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents, list_of_names)
        return df

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)