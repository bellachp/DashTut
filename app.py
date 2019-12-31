# app.py
# for dash tutorial

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')



_external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=_external_stylesheets)

colors = {
    'background': '#F8FFEC',
    'text': '#4F3939'
}


app.layout = html.Div(style={'backgroundColor': colors["background"]}, children=[
    html.H1(
        children="Buenos Días, weoncitos",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(
        children='''
            Welcome to the World of Tomorrow!
            ''',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

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
        }),

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
                ))

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



# main
if __name__ == '__main__':
    app.run_server(debug=True)
