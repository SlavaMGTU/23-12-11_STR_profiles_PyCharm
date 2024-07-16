import pandas as pd

import dash
from dash import dcc, html
from dash import Input, Output, State, callback
from dash import dash_table as dt

import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

app.layout = html.Div(
    [
        dbc.Row(
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Top"),
                    dbc.Input(id="T", placeholder="Project Name"),
                ],
                className="mb-3",
            )
        ),
        dbc.Row(
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Base"),
                    dbc.Input(id="B", placeholder="Project Name"),
                ],
                className="mb-3",
            )
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        dbc.Button(
                            "Add current data to sensitivity table",
                            id="add-row",
                            style={
                                "font-family": "arial",
                                "marginTop": "5px",
                                "marginRight": "10px",
                            },
                            className="d-grid gap-2 col-8",
                            size="sm",
                        ),
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dt.DataTable(
                    id="sensitivity",
                    columns=[
                        {"name": col, "id": col} for col in ["TR", "BR"]
                    ],
                    data=[],
                ),
                dcc.Store(id="button-clicks", data=0),
            ]
        ),
    ], style={"margin": "20%"}
)


@app.callback(
    Output("button-clicks", "data"), Input("add-row", "n_clicks"),
)
def update_button_clicks(n_clicks):
    if n_clicks is None:
        return 0
    return n_clicks


@app.callback(
    Output("sensitivity", "data"),
    Input("button-clicks", "data"),
    State("sensitivity", "data"),
    State(component_id="T", component_property="value"),
    State(component_id="B", component_property="value"),
)
def sensitivityTable(n_clicks, current_data, T, B):
    if n_clicks == 0:
        return dash.no_update

    # Adjusted the keys to match column IDs
    new_row_data = {"TR": T, "BR": B}

    if current_data is None:
        current_data = []

    sensitivity_updated_data = current_data + [new_row_data]

    return sensitivity_updated_data

if __name__ == "__main__":
    app.run_server(port=8054, debug=True)