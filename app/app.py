import sys
sys.path.extend(["pages","."])
import dash
from sql import *
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
#--------------------------------------------------------------------------------------------------------
#-- Front functions
#--------------------------------------------------------------------------------------------------------
def get_navbar(pages)->html.Div:
    """TODO"""
    logo = html.Img(src='assets/logo.png', id='logo')
    items = [
        dbc.DropdownMenuItem(dbc.NavLink(page['name'], href=page['relative_path'])) for page in pages
        ]
    navbar = dbc.NavbarSimple([
        dbc.DropdownMenu(items, label='Pages'),
        ], brand=logo, brand_href='/home', id='header', expand=True)
    return navbar

#--------------------------------------------------------------------------------------------------------
#-- APP init
#--------------------------------------------------------------------------------------------------------
# app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.BOOTSTRAP])
app = dash.Dash(__name__,
                use_pages=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
)

app.layout = html.Div(children=[
    # Header banner
     html.Div(children = [
        get_navbar(dash.page_registry.values()),
        ], style={'width':"100%"}, id='navbar-container'),

    # Page
    dash.page_container,
    # url location
    dcc.Location(id='url')

], id='app-container')


#--------------------------------------------------------------------------------------------------------
#-- CALLBACKS
#--------------------------------------------------------------------------------------------------------

# Redirects user to home page on first app load ('/' -> '/home')
@app.callback(
    Output(component_id='url', component_property='pathname'),
    Input(component_id='url', component_property='pathname')
)
def redirect_to_home(current_pathname):
    if current_pathname != '/':
        raise PreventUpdate
    else:
        return '/home'
#--------------------------------------------------------------------------------------------------------
#-- MAIN
#--------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")

