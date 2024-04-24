import dash
from dash import html, dcc, callback, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from home_manager import get_torrent_list

#------------------------------------------------------------------------------------
#-- Layout
#------------------------------------------------------------------------------------
dash.register_page(__name__)

# Define layout
layout = html.Div([
    ],id='home-content')

#------------------------------------------------------------------------------------
#-- Callbacks
#------------------------------------------------------------------------------------
@callback(
    Output('home-content', 'children'),
    Input('home-content', 'children')
)
def gen_table(dummy):
    df = get_torrent_list()
    # table = dash_table.DataTable(
    #     # id='datatable-interactivity',
    #     columns=[
    #         {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
    #         ],
    #     data=df.to_dict('records'),
    #     filter_action="native",
    #     sort_action="native",
    #     sort_mode="multi",
    #     row_deletable=False,
    #     cell_selectable=False,
    #     selected_columns=[],
    #     selected_rows=[],
    #     page_action="native",
    #     fixed_columns = {'headers': True, 'data': 1},
    #     style_table   = {'minWidth': '100%'},
    #     style_cell={'textAlign': 'left'},
    #     )
    table = dbc.Table.from_dataframe(df)
    return html.Div(table, className='px-1')

