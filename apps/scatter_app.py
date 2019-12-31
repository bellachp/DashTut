# scatter_app.py
# for dash tutorial

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from app import app
from urls import url_paths



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')


layout = html.Div([

    # scatterplot with selection slider
    dcc.Graph(id="graph-with-slider"),
    dcc.RangeSlider(
        id="year-range-slider",
        min=df['year'].min(),
        max=df['year'].max(),
        value=[df['year'].min(), df['year'].max()],
        # value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


# callback for slider scatter
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-range-slider', 'value')])
def updated_scatter(selected_years):
    years_range = [k for k in range(selected_years[0], selected_years[1] + 1)]
    filtered_df = df[df.year.isin(years_range)]
    # filtered_df = df[df.year == selected_years]
    traces = []
    for k in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df.continent == k]
        traces.append(
            dict(
                x=df_by_continent.groupby("country")['gdpPercap'].mean(),
                y=df_by_continent.groupby("country")['lifeExp'].mean(),
                text=df_by_continent["country"],
                mode="markers",
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=k
            )
        )

    result_dict = {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'log', 'title': 'GDP Per Capita',
                   'range': [2.3, 4.8]},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition={'duration': 500}
        )
    }

    return result_dict
