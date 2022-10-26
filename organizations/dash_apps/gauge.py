import datetime
import pathlib

import dash
import gridfs
import pandas as pd
import pymongo
#from bson.json_util import dumps
import pytz
from bson.json_util import dumps
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly
from django.utils.safestring import SafeString, mark_safe
# =============================================================================
from django_plotly_dash import DjangoDash
from collections import deque
from queue import Empty
from queue import Queue
from threading import Thread

from plotly.subplots import make_subplots
from pymongo.change_stream import ChangeStream
import time
import random
from dash.exceptions import PreventUpdate
import requests
import json
from collections import OrderedDict

app = DjangoDash("gauge")
app.layout = html.Div([
html.Div([
        dcc.Graph(id='live-graph-4', animate=True,style={'height':'415px', 'margin-top': '-35px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
]),
    ])


#
# fig.show()

@app.callback(
    Output('live-graph-4', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    fig = go.Figure(go.Indicator(
        mode = "gauge",
        value = 250,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Slightly Warm", 'font': {'size': 24}},
        # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#00733c"},
            'bgcolor': "#fff",
            'borderwidth': 2,
            # 'bordercolor': "gray",
            # 'steps': [
            #     {'range': [0, 250], 'color': 'green'},
            #     # {'range': [250, 400], 'color': 'royalblue'}
            # ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 490}}
    ))

    fig.update_layout(paper_bgcolor = "#fff", font = {'color': "darkblue", 'family': "Arial"})

    return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)