# base_app.py
# for dash tutorial

import dash_core_components as dcc
import dash_html_components as html

from app import app
from urls import url_paths


colors = {
    'background': '#F8FFEC',
    'text': '#4F3939'
}


layout = html.Div(style={'backgroundColor': colors["background"]}, children=[
    html.H2(
        children="Buenos Días, weoncitos",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(
        children='''
            Welcome to the World of Tomorrow!
            ''',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # basic bar chart
    dcc.Graph(
        id="test-graph",
        figure={
            'data':
                [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
            'layout':
                {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {'color': colors['text']},
                    'title': 'A test graph'
                }
        }
    ),

    # path to other pages
    dcc.Link("Scatter Example", href=url_paths["scatter"]),
    html.Br(),
    dcc.Link("Combo Example", href=url_paths["combo"])
])
