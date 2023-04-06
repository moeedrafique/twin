import datetime
import pathlib

import numpy as np
from django.utils import timezone
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

myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:9TInnovations@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol_sim = mydb["simulation_sensor_locations"]
mycol_energy = mydb["energy_building"]

app = DjangoDash("gas_co")
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

now = timezone.now()
datetime_today = now.strftime('%Y-%m-%d')
# today_energy_records = mycol_energy.find({"$or": [{"datetime": {'$gte':'2023-03-01', '$lte': datetime_today}}, {"datetime": {"$exists": True}}]}).sort('_id',-1)
today_energy_records = mycol_energy.find({'ref_id': 'DMC02_Energy', 'datetime': {'$gte':'2023-04-01', '$lte': datetime_today}}).sort('_id',-1)


# # Find documents where the date/time field is in the current month
# query = {"createdAt": {"$gte": first_day, "$lt": next_month_first_day}}
# today_energy_records = mycol_energy.find({"$or": [{"datetime": {'$gte':first_day, '$lte': next_month_first_day}}, {"datetime": {"$exists": True}}]}).sort('_id',-1)

occu_dt = []
for c in today_energy_records:
    occu_dt.append(c)
print(occu_dt)
data = pd.DataFrame(occu_dt)
#
main_data = data['data']
#
gas = []
for i in main_data:
    res = i['gas'] * 0.18
    gas.append(res)
#
average = np.mean(gas)
print(average)

@app.callback(
    Output('live-graph-4', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    fig = go.Figure(go.Indicator(
        mode = "gauge",
        value = average,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "GAS", 'font': {'size': 24, 'color':'white'}},
        # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'bar': {'color': "#38eedf"},
                 }))
    fig.update_layout(paper_bgcolor="#27293d", font={'color': "white", 'family': "Arial"})


    return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)