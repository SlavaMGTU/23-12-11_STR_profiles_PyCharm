@app.callback(
    Output('table_fin', 'children'),
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
                columns = [{'name': col, 'id': col} for col in df_table.columns]
                data = df_table.to_dict('records')

                return dash_table.DataTable(
                    columns=columns,
                    data=data,
                    sort_action='native',  # Разрешение на сортировку в браузере
                    style_table={'overflowX': 'auto'}  # Добавить горизонтальную прокрутку для таблицы
                )

    else:
        return ''