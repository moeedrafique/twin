import pathlib

import dash
import gridfs
import pandas as pd
import pymongo
#from bson.json_util import dumps
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
from pymongo.change_stream import ChangeStream
import time
import random
from dash.exceptions import PreventUpdate
import requests
import json
from collections import OrderedDict
# =============================================================================
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()
import threading

myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol_sim = mydb["simulation_sensor_locations"]

app = DjangoDash('inlet2')

app.layout = html.Div([
html.Div([
        dcc.Graph(id='live-graph-2', animate=True,style={'height': '320px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
]),
    ])

xx = []
yy = []

def read_stream():
    for change in mycol_sim.watch([{
        '$match': {
            'operationType': {'$in': ['replace', 'insert']},
            'fullDocument.business': 'Digital Media Centre'
        }
    }
    ]
    ):
        x = change["fullDocument"]
        sim_main_data = x['data']
        EG1 = sim_main_data['EG1_1boundary']
        yy.append(EG1)

        time = x['timestamp']
        xx.append(time)

st = Thread(target=read_stream, args=())
st.start()
st.is_alive()

@app.callback(
    Output('live-graph-2', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    ahu=yy
    # print(ahu)
    temp= xx

    data = plotly.graph_objs.Scatter(
        x=list(temp),
        y=list(ahu),
        name='Scatter',
        mode='lines+markers'
    )
    layout = go.Layout(
        # paper_bgcolor='#27293d',
        # plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(temp), max(temp)]),
        yaxis=dict(range=[min(ahu), max(ahu)]),
        # font=dict(color='white'),

    )

    return {'data': [data], 'layout':layout}

