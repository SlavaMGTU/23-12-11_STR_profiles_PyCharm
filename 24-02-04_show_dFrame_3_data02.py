# продолжение файла 24-02-03_read-csv_show-table00.py Для отображения уникальных значений столбца 'кличка' из DataFrame в выпадающем списке в веб-приложении Dash
# добавляю 3 поля
### ОШИБКА ПРИ ЗАПУСКЕ!!!! НО ПОКА не влияет на выбор из списка
# Traceback (most recent call last):
#   File "D:\work\23-12-11_STR_profiles_PyCharm\venv\Lib\site-packages\flask\app.py", line 867, in full_dispatch_request
#     rv = self.dispatch_request()
#          ^^^^^^^^^^^^^^^^^^^^^^^
#   File "D:\work\23-12-11_STR_profiles_PyCharm\venv\Lib\site-packages\flask\app.py", line 852, in dispatch_request
#     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "D:\work\23-12-11_STR_profiles_PyCharm\venv\Lib\site-packages\dash\dash.py", line 1310, in dispatch
#     ctx.run(
#   File "D:\work\23-12-11_STR_profiles_PyCharm\venv\Lib\site-packages\dash\_callback.py", line 457, in add_context
#     flat_output_values = flatten_grouping(output_value, output)
#                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "D:\work\23-12-11_STR_profiles_PyCharm\venv\Lib\site-packages\dash\_grouping.py", line 35, in flatten_grouping
#     validate_grouping(grouping, schema)
#   File "D:\work\23-12-11_STR_profiles_PyCharm\venv\Lib\site-packages\dash\_grouping.py", line 210, in validate_grouping
#     SchemaTypeValidationError.check(grouping, full_schema, path, (tuple, list))
#   File "D:\work\23-12-11_STR_profiles_PyCharm\venv\Lib\site-packages\dash\_grouping.py", line 162, in check
#     raise SchemaTypeValidationError(value, full_schema, path, expected_type)
# dash._grouping.SchemaTypeValidationError: Schema: [<Output child-dropdown.options>, <Output parent1-dropdown.options>, <Output parent2-dropdown.options>]
# Path: ()
# Expected type: (<class 'tuple'>, <class 'list'>)
# Received value of type <class 'NoneType'>:
#     None
# ###
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
        dcc.Dropdown(id='child-dropdown')
    ]),
    html.Div([
        html.Label('Родитель1'),  # Добавляем надпись "Родитель1" над выпадающим списком
        dcc.Dropdown(id='parent1-dropdown')
    ]),
    html.Div([
        html.Label('Родитель2'),  # Добавляем надпись "Родитель2" над выпадающим списком
        dcc.Dropdown(id='parent2-dropdown')
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
    return dropdown_options

# Обратная связь для обновления выпадающих списков
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

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)