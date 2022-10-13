import datetime
import pathlib
from datetime import datetime, timedelta
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

myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol_sim = mydb["simulation_sensor_locations"]

app = DjangoDash("update")
# app = dash.Dash()
app.layout = html.Div([
html.Div([
        dcc.Graph(id='live-graph-3', animate=True,style={'height': '320px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
    ],className="card-header table-card-header mb-3",),
html.Div([
        dcc.Graph(id='live-graph-4', animate=True,style={'height': '320px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
    ],className="card-header table-card-header mb-3",),
html.Div([
        dcc.Graph(id='live-graph-5', animate=True,style={'height': '320px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
    ],className="card-header table-card-header mb-3",),
html.Div([
        dcc.Graph(id='live-graph-6', animate=True,style={'height': '320px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
    ],className="card-header table-card-header mb-3",),
html.Div([
        dcc.Graph(id='live-graph-7', animate=True,style={'height': '320px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
    ],className="card-header table-card-header mb-3",),
    ])

xx = []
SG1 = []
SG2 = []
SG3 = []
SG4 = []
SG5 = []
SG6 = []


SF1 = []
SF2 = []


EG1 = []
FCU_IN = []

AHU_OUT = []
MAIN_DOOR = []

now = timezone.now()
today_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=0)
today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=0)
occupant_records = mycol_sim.find({'ref_id': 'DMC02-CWS', 'timestamp': {'$gte': today_start, '$lte':today_end}}).sort('_id',-1).limit(30)

occu_dt = []
for c in occupant_records:
    occu_dt.append(c)
# print(len(occu_dt))
data = pd.DataFrame(occu_dt)

main_data = data['data']

for i in main_data:
    res = i['SG1_1boundary']
    SG1.append(res)

for i in main_data:
    res = i['SG2_2boundary']
    SG2.append(res)

for i in main_data:
    res = i['SG3_2boundary']
    SG3.append(res)

for i in main_data:
    res = i['SG4_2boundary']
    SG4.append(res)

for i in main_data:
    res = i['SG5_2boundary']
    SG5.append(res)

for i in main_data:
    res = i['SG6_2boundary']
    SG6.append(res)

for i in main_data:
    res = i['SF1_2boundary']
    SF1.append(res)

for i in main_data:
    res = i['SF2_2boundary']
    SF2.append(res)

for i in main_data:
    res = i['EG1_1boundary']
    EG1.append(res)

for i in main_data:
    res = i['FCU_INboundary']
    FCU_IN.append(res)

for i in main_data:
    res = i['AHU_OUTboundary']
    AHU_OUT.append(res)

for i in main_data:
    res = i['MAIN_DOORboundary']
    MAIN_DOOR.append(res)

for t in data['timestamp']:
    # print(t)
    xx.append(t)
# print(len(xx))


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
        sf1 = i['SF1_2boundary']
        # print(sf1)
        SF1.append(sf1)

        sf2 = i['SF2_2boundary']
        SF2.append(sf2)

        sg1 = i['SG1_1boundary']
        SG1.append(sg1)

        sg2 = i['SG2_2boundary']
        SG2.append(sg2)

        sg3 = i['SG3_2boundary']
        SG3.append(sg3)

        sg4 = i['SG4_2boundary']
        SG4.append(sg4)

        sg5 = i['SG5_2boundary']
        SG5.append(sg5)

        sg6 = i['SG6_2boundary']
        SG6.append(sg6)

        eg1 = i['EG1_1boundary']
        EG1.append(eg1)

        ahu_out = i['AHU_OUTboundary']
        AHU_OUT.append(ahu_out)

        fcu_in = i['FCU_INboundary']
        FCU_IN.append(fcu_in)

        main_door = i['MAIN_DOORboundary']
        MAIN_DOOR.append(main_door)

        time = x['timestamp']
        xx.append(time)

st = Thread(target=read_stream, args=())
st.start()
st.is_alive()

@app.callback(
    Output('live-graph-3', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    # ahu=yy
    # # print(ahu)
    temp= xx

    fig = plotly.graph_objs.Figure()
    fig.add_trace(go.Scatter(x=list(temp), y=list(SG2), name='SG2_2'))
    fig.add_trace(go.Scatter(x=list(temp), y=list(SG3), name='SG3_2'))
    fig.add_trace(go.Scatter(x=list(temp), y=list(SG4), name='SG4_2'))
    fig.add_trace(go.Scatter(x=list(temp), y=list(SG5), name='SG5_2'))
    fig.add_trace(go.Scatter(x=list(temp), y=list(SG6), name='SG6_2'))
    fig.update_layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        # xaxis=dict(range=[min(temp), max(temp)]),
        # yaxis=dict(range=[min(ahu), max(ahu)]),
        font=dict(color='white'),
        xaxis={
            "title": "Solar Radiation",
            # "showgrid": False,
            # "showline": False,
            # "fixedrange": True,
        },
        yaxis={
            # "showgrid": False,
            # "showline": False,
            # "zeroline": False,
            "title": "Temperature(F)",
            # "fixedrange": True,
        },
    #
    )

    return fig


@app.callback(
    Output('live-graph-4', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter_2(n):
    # ahu=yy
    # # print(ahu)
    temp= xx

    fig = plotly.graph_objs.Figure()
    fig.add_trace(go.Scatter(x=list(temp), y=list(SF1), name='SF1_2'))
    fig.add_trace(go.Scatter(x=list(temp), y=list(SF2), name='SF2_2'))
    fig.update_layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        # xaxis=dict(range=[min(temp), max(temp)]),
        # yaxis=dict(range=[min(ahu), max(ahu)]),
        font=dict(color='white'),
        xaxis={
            "title": "Solar Radiation",
            # "showgrid": False,
            # "showline": False,
            # "fixedrange": True,
        },
        yaxis={
            # "showgrid": False,
            # "showline": False,
            # "zeroline": False,
            "title": "Temperature(F)",
            # "fixedrange": True,
        },
    #
    )

    return fig


@app.callback(
    Output('live-graph-5', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter_3(n):
    # ahu=yy
    # # print(ahu)
    temp= xx

    fig = plotly.graph_objs.Figure()
    fig.add_trace(go.Scatter(x=list(temp), y=list(EG1), name='EG1_1'))
    fig.add_trace(go.Scatter(x=list(temp), y=list(FCU_IN), name='FCU_IN'))
    fig.update_layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        # xaxis=dict(range=[min(temp), max(temp)]),
        # yaxis=dict(range=[min(ahu), max(ahu)]),
        font=dict(color='white'),
        xaxis={
            "title": "Solar Radiation",
            # "showgrid": False,
            # "showline": False,
            # "fixedrange": True,
        },
        yaxis={
            # "showgrid": False,
            # "showline": False,
            # "zeroline": False,
            "title": "Temperature(F)",
            # "fixedrange": True,
        },
    #
    )

    return fig


@app.callback(
    Output('live-graph-6', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter_4(n):
    # ahu=yy
    # # print(ahu)
    temp= xx

    fig = plotly.graph_objs.Figure()
    fig.add_trace(go.Scatter(x=list(temp), y=list(AHU_OUT), name='AHU_OUT'))
    fig.update_layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        # xaxis=dict(range=[min(temp), max(temp)]),
        # yaxis=dict(range=[min(ahu), max(ahu)]),
        font=dict(color='white'),
        xaxis={
            "title": "Solar Radiation",
            # "showgrid": False,
            # "showline": False,
            # "fixedrange": True,
        },
        yaxis={
            # "showgrid": False,
            # "showline": False,
            # "zeroline": False,
            "title": "Temperature(F)",
            # "fixedrange": True,
        },
    #
    )

    return fig

@app.callback(
    Output('live-graph-7', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter_5(n):
    # ahu=yy
    # # print(ahu)
    temp= xx

    fig = plotly.graph_objs.Figure()
    fig.add_trace(go.Scatter(x=list(temp), y=list(MAIN_DOOR), name='MAIN_DOOR'))
    fig.update_layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        # xaxis=dict(range=[min(temp), max(temp)]),
        # yaxis=dict(range=[min(ahu), max(ahu)]),
        font=dict(color='white'),
        xaxis={
            "title": "Solar Radiation",
            "showgrid": False,
            "showline": False,
            "fixedrange": True,
        },
        yaxis={
            "showgrid": False,
            "showline": False,
            "zeroline": False,
            "title": "Temperature(F)",
            "fixedrange": True,
        },
    #
    )

    return fig
# if __name__ == '__main__':
#     app.run_server(debug=True)



    # fig = make_subplots(
    #     specs=[[{"secondary_y":True}]])
    #
    # fig.add_trace(go.Scatter(x=list(temp), y=list(SG1)),secondary_y=False)
    # fig.add_trace(go.Scatter(x=list(temp), y=list(SG2)), secondary_y=False)
    # fig.add_trace(go.Scatter(x=list(temp), y=list(SG3)), secondary_y=False)
    # fig.add_trace(go.Scatter(x=list(temp), y=list(SG4)), secondary_y=False)
    # fig.add_trace(go.Scatter(x=list(temp), y=list(SG5)), secondary_y=False)
    # fig.add_trace(go.Scatter(x=list(temp), y=list(SG6)), secondary_y=False)
    #
    # fig.update_layout(height=500, width=1000,
    #                   title_text="Multiple Subplots with Titles")
    #
    # fig.show()

















#
#
#
#
# import datetime
# import pathlib
#
# import dash
# import gridfs
# import pandas as pd
# import pymongo
# #from bson.json_util import dumps
# import pytz
# from bson.json_util import dumps
# from dash import dcc
# from dash import html
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go
# import plotly
# from django.utils.safestring import SafeString, mark_safe
# # =============================================================================
# from django_plotly_dash import DjangoDash
# from collections import deque
# from queue import Empty
# from queue import Queue
# from threading import Thread
#
# from plotly.subplots import make_subplots
# from pymongo.change_stream import ChangeStream
# import time
# import random
# from dash.exceptions import PreventUpdate
# import requests
# import json
# from collections import OrderedDict
# # =============================================================================
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("./data").resolve()
# import threading
#
# myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
# mydb = myclient["twin_dynamics"]
# mycol_sim = mydb["simulation_sensor_locations"]
#
# app = dash.Dash()
#
# app.layout = html.Div([
# html.Div([
#         dcc.Graph(id='live-graph-3', animate=True,style={'height': '320px'}),
#         dcc.Interval(
#             id='graph-update',
#             interval=75000,
#             n_intervals=0
#         ),
# ]),
#     ])
#
# xx = []
# SF1 = []
# SF2 = []
#
#
# today = datetime.date.today()
# yesterday = datetime.date.today() - datetime.timedelta(hours=6)
# # yesterday = datetime.date.today() - datetime.timedelta(days=1)
#
# start = datetime.datetime.combine(yesterday, datetime.time(0, 0)).replace(tzinfo=pytz.utc)
# end = datetime.datetime.combine(today, datetime.time(0, 0)).replace(tzinfo=pytz.utc)
# occupant_records = mycol_sim.find({'ref_id': 'DMC02-CWS'}).limit(50)
#
# occu_dt = []
# for c in occupant_records:
#     occu_dt.append(c)
# # print(len(occu_dt))
# data = pd.DataFrame(occu_dt)
#
# main_data = data['data']
#
# for i in main_data:
#     res = i['SF1_2boundary']
#     SF1.append(res)
#
# for i in main_data:
#     res = i['SF2_2boundary']
#     SF2.append(res)
#
# for t in data['timestamp']:
#     # print(t)
#     xx.append(t)
# # print(len(xx))
#
#
# # def read_stream():
# #     for change in mycol_sim.watch([{
# #         '$match': {
# #             'operationType': {'$in': ['replace', 'insert']},
# #             'fullDocument.business': 'Digital Media Centre'
# #         }
# #     }
# #     ]
# #     ):
# #         x = change["fullDocument"]
# #         sim_main_data = x['data']
# #         add_sf = sim_main_data['SF1_2boundary'] + sim_main_data['SF2_2boundary']
# #         mean_s_f = add_sf / 2
# #         SF1.append(mean_s_f)
# #
# #         time = x['timestamp']
# #         xx.append(time)
# #
# # st = Thread(target=read_stream, args=())
# # st.start()
# # st.is_alive()
#
# @app.callback(
#     Output('live-graph-3', 'figure'),
#     [Input('graph-update', 'n_intervals')]
# )
# def update_graph_scatter(n):
#     ahu=SF1
#     # print(ahu)
#     temp= xx
#     fig = make_subplots(
#         specs=[[{"secondary_y":True}]])
#
#     fig.add_trace(go.Scatter(x=list(temp), y=list(SF1)),secondary_y=False)
#     fig.add_trace(go.Scatter(x=list(temp), y=list(SF2)), secondary_y=False)
#
#     fig.update_layout(height=500, width=700,
#                       title_text="Multiple Subplots with Titles")
#
#     fig.show()
#
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)