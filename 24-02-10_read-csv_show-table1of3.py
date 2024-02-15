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
        multiple=False
    ),
    html.Div(id='output-data-upload'),
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
            return df  # Возвращаем DataFrame вместо dropdown_options
        else:
            return html.Div('Unsupported file format')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        )
    ])


# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)