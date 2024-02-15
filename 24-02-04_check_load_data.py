import dash
from dash import dcc, html
import pandas as pd
import base64
import io
from dash import dash_table

# Создание экземпляра приложения Dash
app = dash.Dash(__name__)

# Отображение меню выбора файла
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        multiple=False
    ),
    html.Div(id='output-data-upload')
])

# Функция для загрузки файла и отображения данных в виде таблицы
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Если файл имеет расширение .csv, считываем его, используя pandas и модуль io
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8'))
            )
        else:
            return html.Div('Unsupported file format')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6('Processed data from file:'),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        )
    ])

# Обратная связь для обновления состояния отображаемых данных
@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
              [dash.dependencies.Input('upload-data', 'contents'),
               dash.dependencies.Input('upload-data', 'filename')])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(list_of_contents, list_of_names)
        ]
        return children

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
