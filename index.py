# index.py
# index layout for tutorial

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from urls import url_paths
from apps import base_app, scatter_app, combo_app


app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]
)


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def render_page(pathname):
    if pathname == url_paths["index"] or pathname == url_paths["home"]:
        return base_app.layout
    elif pathname == url_paths["scatter"]:
        return scatter_app.layout
    elif pathname == url_paths["combo"]:
        return combo_app.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
