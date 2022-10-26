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

app = dash.Dash()
app.layout = html.Div(
    html.Div([

        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 3000,  # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    data = {
        'time': [],
        'PH': [],
        'CON': [],
        'TOTAL': [],
        'VOLATILE': [],
    }

    # Collect some data
    for i in range(9):
        time = datetime.datetime.now() - datetime.timedelta(seconds=i * 20)
        ph = random.randint(8, 13)
        con = random.randint(10, 20)
        total = random.randint(1, 5)
        volatile = random.randint(5, 10)
        data['PH'].append(ph)
        data['CON'].append(con)
        data['TOTAL'].append(total)
        data['VOLATILE'].append(volatile)
        data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=2, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }

    fig.add_trace({
        'x': data['time'],
        'y': data['PH'],
        'name': 'PH',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['time'],
        'y': data['CON'],
        'name': 'Conductivity',
        'mode': 'lines+markers',
        'type': 'scatter',

    }, 2, 1)
    fig.append_trace({
        'x': data['time'],
        'y': data['TOTAL'],
        'name': 'Total Suspended Solids',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 2)
    fig.append_trace({
        'x': data['time'],
        'y': data['VOLATILE'],
        'name': 'Volatile Suspended Solids',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 2)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
