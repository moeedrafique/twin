import pathlib
from datetime import datetime, timedelta
import dash
import gridfs
import pandas as pd
import pymongo
import datetime
#from bson.json_util import dumps
import pytz
from bson.json_util import dumps
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly
from django.utils import timezone
import dash_extendable_graph as deg
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

myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:9TInnovations@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol_sim = mydb["simulation_sensor_locations"]

app = DjangoDash('temp_vent_data')

app.layout = html.Div([
html.Div([
        dcc.Graph(id='live-graph-2', animate=True,style={'height': '335px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
]),
    ])

xx = []
yy = []


now = timezone.now()
today_start = now - timedelta(days=1)
today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=0)
occupant_records = mycol_sim.find({'ref_id': 'DMC02-CWS', 'timestamp': {'$gte': today_start, '$lte':today_end}}).sort('timestamp',-1)
print(occupant_records)
occu_dt = []
for c in occupant_records:
    occu_dt.append(c)
# print(len(occu_dt))
data = pd.DataFrame(occu_dt)

main_data = data['data']

for i in main_data:
    res = i["sf1_2"] + i["sf2_2"] + i["ahu_out"] + i['sg1_1'] + i['sg2_2'] + i['sg3_2'] + i['sg4_2'] + i['sg5_2'] + i['sg6_2']
    mean_first_inlet = res / 9
    yy.append(mean_first_inlet)
# print(len(yy))
# print(np.mean(yy))

for t in data['timestamp']:
    # print(t)
    xx.append(t)
# print(len(xx))

new_time = []
new_data = []


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
        i = x['data']
        add_sg = i["sf1_2"] + i["sf2_2"] + i["ahu_out"] + i['sg1_1'] + i['sg2_2'] + i['sg3_2'] + i['sg4_2'] + i['sg5_2'] + i['sg6_2']
        mean_sg = add_sg / 9
        yy.append(mean_sg)

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

    data = plotly.graph_objs.Bar(
        x=list(temp),
        y=list(ahu),
        marker_color ='black',
        marker_line_color='#000',
        #name='Scatter',
        #mode='Bars'
    )
    layout = go.Layout(
        # paper_bgcolor='#27293d',
        # plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(temp), max(temp)]),
        yaxis=dict(range=[min(ahu), max(ahu)]),
        # font=dict(color='white'),

    )

    return {'data': [data], 'layout':layout}


