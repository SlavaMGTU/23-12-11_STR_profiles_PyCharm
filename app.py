import dash
from dash import html, dcc

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Hello World!'),
    dcc.Graph(
        figure={
            'data': [{
                'x': [1, 2, 3],
                'y': [4, 1, 2],
                'type': 'bar',
                'name': 'Example'
            }],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)