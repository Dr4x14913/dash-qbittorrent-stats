import sys
sys.path.extend(["pages","."])
import dash
from sql import *
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from backoffice_manager import get_disabled_pages

#--------------------------------------------------------------------------------------------------------
#-- SQL init
#--------------------------------------------------------------------------------------------------------

#Establish the connection to MariaDB
db = Sql(MYSQL_DATABASE, DB_HOST='db', DB_USER=MYSQL_USER, DB_PASS=MYSQL_PASSWORD)
print("Connection successful!")

db.insert(f"""
    INSERT INTO users (username, password)
    SELECT * FROM (SELECT 'admin' as username, '123' as password) AS tmp
    WHERE NOT EXISTS (
        SELECT username FROM users WHERE username = 'admin'
    ) LIMIT 1
""")
print('Admin user created!')
db.close()

#--------------------------------------------------------------------------------------------------------
#-- Front functions
#--------------------------------------------------------------------------------------------------------

def get_navbar(pages, current_user)->html.Div:
    """TODO"""
    logged_txt = "Not logged" if current_user is None else current_user
    logo = html.Img(src='assets/logo.png', id='logo')
    user = dbc.NavItem(dbc.NavLink(logged_txt), id="user-display")
    items = [
        dbc.DropdownMenuItem(dbc.NavLink(page['name'], href=page['relative_path']))
        for page in pages if not(
            page["name"] == "Home" or # home n'est pas pris en compte dans la navbar
            page['name'] == 'Backoffice' and current_user != 'admin' or
            page['name'].lower() in get_disabled_pages()
          )
    ]
    navbar = dbc.NavbarSimple([
        dbc.DropdownMenu(items, label='Pages'),
        user,
        ], brand=logo, brand_href='/home', id='header', expand=True)
    return navbar

#--------------------------------------------------------------------------------------------------------
#-- APP init
#--------------------------------------------------------------------------------------------------------
# app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.BOOTSTRAP])
app = dash.Dash(__name__,
                use_pages=True,
                external_stylesheets=[dbc.themes.QUARTZ, dbc.icons.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
)

app.layout = html.Div(children=[
    # Header banner
     html.Div(children = [
        get_navbar(dash.page_registry.values(), None),
        ], style={'width':"100%"}, id='navbar-container'),

    # Page
    dash.page_container,

    # Properties storage
    # current user
    dcc.Store(id='CURRENT_USER', storage_type='session', data=None),
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

# Redirects user to home page on first app load ('/' -> '/home')
@app.callback(
    Output(component_id='navbar-container', component_property='children'),
    Input(component_id='CURRENT_USER', component_property='data')
)
def navbar_callback(current_user):
    return get_navbar(dash.page_registry.values(), current_user)

#--------------------------------------------------------------------------------------------------------
#-- MAIN
#--------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")

