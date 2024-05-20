import dash
from sql import Sql
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_ag_grid as dag
import re
from app_manager import get_torrent_list

#--------------------------------------------------------------------------------------------------------
#-- Tools
#--------------------------------------------------------------------------------------------------------
def custom_sort(item):
    if isinstance(item, int):
        return (0, item) # 0 for integers
    else:
        return (1, item) # 1 for strings

def clean_str(string):
    normal_string = re.sub(r"[^A-Z0-9_[\]\.(){} -]", "_",string,0,re.IGNORECASE)
    return normal_string

#--------------------------------------------------------------------------------------------------------
#-- APP init
#--------------------------------------------------------------------------------------------------------
# app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.BOOTSTRAP])
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
)

app.layout = dbc.Container([
    dbc.Row(dbc.Col([dbc.Button("import data", id ="btn-import"), html.Div(id='modal-import')])),
    dbc.Row(dbc.Col(dcc.Loading(html.Div([], id='table-torrents')))),
], id='app-container')


#--------------------------------------------------------------------------------------------------------
#-- Callbacks
#--------------------------------------------------------------------------------------------------------
@callback(
    Output('table-torrents', 'children'),
    Input ('table-torrents', 'children'),
)
def display_table(dummy):
    return dbc.Table.from_dataframe(get_torrent_list())

@callback(
    Output('modal-import', 'children'),
    Input('btn-import', 'n_clicks'),
)
def display_import_modal(clicks):
    if clicks is None:
        raise PreventUpdate
    modal = dbc.Modal([
        dbc.ModalHeader("Import csv data"),
        dbc.ModalBody(dcc.Loading(html.Div([
            html.P('Correct columns are: name, uploaded, downloaded, ratio, size, day'),
            dbc.Textarea(id='txt-import'),
        ]), id='modal-import-body')),
        dbc.ModalFooter(dbc.Button('Import !', id='btn-trigger-import'))
        ], is_open=True)
    return modal

@callback(
    Output('btn-trigger-import', 'disabled'),
    Input('btn-trigger-import', 'n_clicks'),
)
def disable_btn_import(click):
    if click is None:
        raise PreventUpdate
    return True

@callback(
    Output('modal-import-body', 'children'),
    Input('btn-trigger-import', 'n_clicks'),
    State('txt-import', 'value'),
    prevent_initial_call=True,
)
def process_import(click, txt):
    if click is None:
        raise PreventUpdate

    struct = {
            'name'       : 'empty',
            'uploaded'   : 'empty',
            'downloaded' : 'empty',
            'ratio'      : 'empty',
            'size'       : 'empty',
            'day'        : 'empty',
            }
    try:
        rows = txt.split('\n')
        rows = [r.split(';') for r in rows]
        headers = rows[0]
        for h in headers:
            if h.lower() in struct:
                struct[h.lower()] = headers.index(h)

        keys_order = ', '.join(dict(sorted(struct.items(), key=lambda x: custom_sort(x[1]))).keys())
        db = Sql('website')
        for r in rows[1:]:
            r = [f"'{clean_str(i)}'" if j==struct['name'] else f"'{i}'" for i,j in zip(r, range(len(r)))] + ["''" for i in range(len(struct) - len(r))]
            req = f"INSERT INTO torrents ({keys_order}) VALUES ({', '.join(r)})"
            db.insert(req)

        db.close()

        return_obj = dbc.Alert(f"All good !", color="success")
    except Exception as e:
        return_obj = dbc.Alert(f"Something went wrong: {e}", color="danger")

    return return_obj





#--------------------------------------------------------------------------------------------------------
#-- MAIN
#--------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")

