from datetime import datetime, timedelta
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
from django.utils import timezone
from django.conf import settings
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
# =============================================================================
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()
import threading
#
myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:9TInnovations@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol_sim = mydb["simulation_sensor_locations"]
mycol_energy = mydb["energy_building"]
#
app = DjangoDash("energy")

app.layout = html.Div([
html.Div([
        dcc.Graph(id='live-graph', animate=True,style={'height': '395px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
]),
    ])
#
# xx = []
# SF1 = []
# SF2 = []
#
#
now = timezone.now()
previous_date = now - timedelta(days=30)
previous_date_str = previous_date.strftime('%Y-%m-%d')
datetime_today = now.strftime('%Y-%m-%d')
today_energy_records = mycol_energy.find({'ref_id': 'DMC02_Energy', 'datetime': {'$gte':previous_date_str, '$lte': datetime_today}}).sort('_id',-1)


# today_energy_records = mycol_energy.aggregate([
#     {
#         "$project": {
#             "y": {"$year": "$timestamp"},
#             "m": {"$month": "$timestamp"},
#             "d": {"$dayOfMonth": "$timestamp"},
#             "h": {"$hour": "$timestamp"}
#         }
#     },
#     {
#         "$match":
#             {'ref_id': 'DMC02', "d": {"$gte": 10, "$lte": 11}}
#     },
#     {
#         "$group":
#             {"_id": {"year": "$y", "month": "$m", "day": "$d", "hour": "$h"}
#
#              }
#     }
#
# ])



occu_dt = []
for c in today_energy_records:
    occu_dt.append(c)
# print(len(occu_dt))
data = pd.DataFrame(occu_dt)
#
main_data = data['data']
#
gas = []
for i in main_data:
    res = i['gas']
    gas.append(res)
#
elec = []
for i in main_data:
    res = i['electricity']
    elec.append(res)
# print(len(elec))
# print(elec)
#
time = []
for t in data['datetime']:
    # print(t)
    time.append(t)
# print(len(time))
# print(time)
#
#
def read_stream():
    for change in mycol_energy.watch([{
        '$match': {
            'operationType': {'$in': ['replace', 'insert']},
            'fullDocument.business': 'Digital Media Centre'
        }
    }
    ]
    ):
        x = change["fullDocument"]
        sim_main_data = x['data']

        add_elec = sim_main_data['electricity']
        elec.append(add_elec)

        add_gas = sim_main_data['gas']
        gas.append(add_gas)

        add_time = x['datetime']
        time.append(add_time)


st = Thread(target=read_stream, args=())
st.start()
st.is_alive()

button_layer_1_height = 1.12
button_layer_2_height = 1.5
# stackData = pd.DataFrame(stackData)
@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):


    trace1 = go.Bar(
        name="Electricity",
        x=list(time),
        y=list(elec),
        offsetgroup=0,
        marker_color = '#f4c142',
        # text = "Electricity "
    ),
    trace2 = go.Bar(
        name="Gas",
        x=list(time),
        y=list(gas),
        offsetgroup=0,
        marker_color = '#758cec',
        # text = "Gas"
    ),
    fig = make_subplots()
    fig.add_traces(trace1)
    fig.add_traces(trace2)
    fig.update_layout(
        # width=1500,
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        # xaxis=dict(range=[min(temp), max(temp)]),
        # yaxis=dict(range=[min(ahu), max(ahu)]),
        font=dict(color='white'),
        xaxis={
            # "title": "Solar Radiation",
            # "showgrid": False,
            # "showline": False,
            # "fixedrange": True,
        },
        yaxis={
            # "showgrid": False,
            # "showline": False,
            # "zeroline": False,
            "title": "Energy Consumption(kWh)",
            #"range": [0, 4]
            # "fixedrange": True,
        },
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                buttons=list([
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True]},
                               {"title": "Both"}
                               ]),
                    dict(label="Electricity",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Electricity",
                                }]),
                    dict(label="Gas",
                         method="update",
                         args=[{"visible": [False, True]},
                               {"title": "Gas",
                                }]),
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="left",
                y=button_layer_2_height,
                yanchor="top",
                font=dict(color='#bdbdbd'),
            )
        ]
    #
    )

    return fig