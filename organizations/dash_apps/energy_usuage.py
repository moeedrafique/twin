import calendar
import datetime
# from datetime import datetime, timedelta
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
from dash.dependencies import Input, Output, State
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
# Get the current year and month
current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month


# Aggregate the collection to extract the year and month values from the datetime fields
result = mycol_energy.aggregate([
    {'$addFields': {
        'dateObj': {'$toDate': '$datetime'}
    }},
    {'$project': {
        'year': {'$year': '$dateObj'},
        'month': {'$month': '$dateObj'}
    }},
    {'$match': {
        '$or': [
            {'year': {'$gt': current_year}},
            {'year': current_year, 'month': {'$lte': current_month}}
        ]
    }},
    {'$sort': {'year': 1, 'month': 1}},
    {'$group': {
        '_id': {'year': '$year', 'month': '$month'},
        'count': {'$sum': 1}
    }}
])
# Extract the unique months from the MongoDB result
months = []


for doc in result:
    year = doc['_id']['year']
    month = doc['_id']['month']
    month_name = calendar.month_name[month]
    months.append({'label': f"{month_name}", 'value': f"{year}-{month:02d}"})

# print(months)
labels = [d['label'] for d in months]
# print(labels)
months_sorted = sorted(labels, key=lambda x: datetime.datetime.strptime(x, "%B").month)
# print(months_sorted)

app = DjangoDash("energy_usuage")

app.layout = html.Div([
html.Div([
        dcc.Dropdown(
            id='month-dropdown',
            options=months,
            value=months[0]['value']
        ),
        dcc.Graph(id='live-graph', animate=True,style={'height': '500px'}),

]),
html.Div(style={'display': 'flex'},children=[

        dcc.Graph(id='live-graph-4', animate=True, style={'height': '415px', 'margin-top': '-35px', 'width': '50%'}),
        dcc.Graph(id='live-graph-5', animate=True, style={'height': '415px', 'margin-top': '-35px', 'width': '50%'}),
]),
    ])
#
# xx = []
# SF1 = []
# SF2 = []
#
#
now = timezone.now()
year = now.year
month = now.month

# Get the first day of the current month
first_day = datetime.datetime(year, month, 1).strftime('%Y-%m-%d')
datetime_today = now.strftime('%Y-%m-%d')

button_layer_1_height = 1.12
button_layer_2_height = 1.5
# stackData = pd.DataFrame(stackData)
@app.callback(
    Output('live-graph', 'figure'),
    Output('live-graph-4', 'figure'),
    Output('live-graph-5', 'figure'),
    [Input('month-dropdown', 'value')],
)
def update_graph(selected_month):
    year, month = selected_month.split("-")
    month_num = int(month)
    start_date = datetime.datetime(current_year, month_num, 1)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date = start_date + datetime.timedelta(days=calendar.monthrange(current_year, month_num)[1])
    end_date_str = end_date.strftime('%Y-%m-%d')
    # filter the data based on the selected month
    print(current_month)
    if month_num == current_month:
        filtered_data = mycol_energy.find({'ref_id': 'DMC02_Energy', 'datetime': {'$gte':first_day, '$lte':datetime_today}}).sort('_id',-1)
    else:
        filtered_data = mycol_energy.find({'ref_id': 'DMC02_Energy', 'datetime': {'$gte':start_date_str, '$lte':end_date_str}}).sort('_id',-1)
    occu_dt = []
    for c in filtered_data:
        occu_dt.append(c)
    # print(occu_dt)
    data = pd.DataFrame(occu_dt)
    #
    main_data = data['data']
    #
    gas = []
    for i in main_data:
        res = i['gas']
        gas.append(res)

    average_gas = np.mean(gas)
    #
    elec = []
    for i in main_data:
        res = i['electricity']
        elec.append(res)
    # print(len(elec))
    print(elec)

    average = np.mean(elec)
    #
    time = []
    for t in data['datetime']:
        # print(t)
        time.append(t)

    trace1 = go.Bar(
        name="Electricity",
        x=list(time),
        y=list(elec),
        offsetgroup=0,
        marker_color='#f4c142',
        # text = "Electricity "
    ),
    trace2 = go.Bar(
        name="Gas",
        x=list(time),
        y=list(gas),
        offsetgroup=0,
        marker_color='#758cec',
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
            "range": [min(time), max(time)],
            # "fixedrange": True,
        },
        yaxis={
            # "showgrid": False,
            # "showline": False,
            # "zeroline": False,
            "title": "Energy Consumption(kWh)",
            # "range": [0, 4]
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

    fig2 = go.Figure(go.Indicator(
        mode = "gauge",
        value = average,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "ELECTRICITY", 'font': {'size': 24, 'color':'white'}},
        # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'bar': {'color': "#d8eb4d"},
                 }))
    fig2.update_layout(paper_bgcolor="#27293d", font={'color': "white", 'family': "Arial"})

    fig3 = go.Figure(go.Indicator(
        mode = "gauge",
        value = average_gas,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "GAS", 'font': {'size': 24, 'color':'white'}},
        # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'bar': {'color': "#38eedf"},
                 }))
    fig3.update_layout(paper_bgcolor="#27293d", font={'color': "white", 'family': "Arial"})

    # updated_fig = create_graph(filtered_data)
    return fig, fig2, fig3