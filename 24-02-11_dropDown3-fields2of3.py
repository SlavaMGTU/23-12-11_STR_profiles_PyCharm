# выбор из загруженного датафрейма нужные строки по имени

from dash import Dash, dcc, html, Input, Output,callback
import pandas as pd

data = {'id': [1, 2, 3], 'кличка': ['Барсик', 'Мурзик', 'Рыжик2']}
df = pd.DataFrame(data)


app = Dash(__name__)
app.layout = html.Div([
    html.Header('My DropDown'),
    dcc.Dropdown(id = 'mydropdown',
                 options=df['кличка'].unique(),
                 placeholder="Select child"),
    html.Div(id='dd-output-container'),
])


@callback(
    Output('dd-output-container', 'children'),
    Input('mydropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run(debug=True)
