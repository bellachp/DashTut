# combo_app.py
# combo scatter & line for interactive viz

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from app import app


df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')


available_indicators = df["Indicator Name"].unique()

# app layout
layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ), style={'padding': '20px 40px'}),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'padding': '0px 10px 20px 10px'}),

    html.Div([
        html.Div([
            dcc.Graph(id='x-time-series'),
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='y-time-series'),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={'padding': '10px'})

])


# function to update combo scatter graph
@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-xaxis-type', 'value'),
     Input('crossfilter-yaxis-type', 'value'),
     Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]

    graph_data = {
        'data': [dict(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }

    return graph_data


# function to create secondary graphs
def create_time_series(dff, axis_type, title):
    ts_data = {
        'data': [dict(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

    return ts_data



@app.callback(
    Output('x-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
     Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-xaxis-type', 'value')])
def update_x_timeseries(hover_data, xaxis_column_name, axis_type):
    country_name = hover_data['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    Output('y-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-yaxis-type', 'value')])
def update_y_timeseries(hover_data, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hover_data['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)
