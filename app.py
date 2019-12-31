# app.py
# for dash tutorial

import dash


_external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=_external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
