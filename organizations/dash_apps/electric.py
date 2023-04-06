from datetime import datetime, timedelta
import pathlib

import dash
import gridfs
import numpy as np
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
# from django.conf import settings
# from django.utils.safestring import SafeString, mark_safe
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

app = DjangoDash("electric")
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
year = now.year
month = now.month

# Get the first day of the current month
first_day = datetime(year, month, 1)

# Get the first day of the next month
if month == 12:
    next_month = 1
    next_year = year + 1
else:
    next_month = month + 1
    next_year = year
next_month_first_day = datetime(next_year, next_month, 1)

datetime_today = now.strftime('%Y-%m-%d')
# today_energy_records = mycol_energy.find({"$or": [{"datetime": {'$gte':'2023-03-01', '$lte': datetime_today}}, {"datetime": {"$exists": True}}]}).sort('_id',-1)
today_energy_records = mycol_energy.find({'ref_id': 'DMC02_Energy', 'datetime': {'$gte':'2023-04-01', '$lte': datetime_today}}).sort('_id',-1)

# Get the current month and year


# # Find documents where the date/time field is in the current month
# query = {"createdAt": {"$gte": first_day, "$lt": next_month_first_day}}
# today_energy_records = mycol_energy.find({"$or": [{"datetime": {'$gte':first_day, '$lte': next_month_first_day}}, {"datetime": {"$exists": False}}]}).sort('_id',-1)

occu_dt = []
for c in today_energy_records:
    occu_dt.append(c)
# print(occu_dt)
data = pd.DataFrame(occu_dt)
#
main_data = data['data']
#
elec = []
for i in main_data:
    res = i['electricity']
    elec.append(res)

average = np.mean(elec)
print(average)
#
# fig.show()

@app.callback(
    Output('live-graph-4', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    fig = go.Figure(go.Indicator(
        mode = "gauge",
        value = average,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "ELECTRICITY", 'font': {'size': 24, 'color':'white'}},
        # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'bar': {'color': "#d8eb4d"},
                 }))
    fig.update_layout(paper_bgcolor="#27293d", font={'color': "white", 'family': "Arial"})


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)