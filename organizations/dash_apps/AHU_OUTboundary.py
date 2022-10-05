import pathlib

import dash
import gridfs
import datetime
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
# =============================================================================
from django_plotly_dash import DjangoDash
from threading import Thread
# =============================================================================
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()
import threading

myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol_sim = mydb["simulation_sensor_locations"]

app = DjangoDash('example')

app.layout = html.Div([
html.Div([
        dcc.Graph(id='live-graph', animate=True,style={'height': '350px'}),
        dcc.Interval(
            id='graph-update',
            interval=75000,
            n_intervals=0
        ),
]),
    ])

xx = []
yy = []

today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(hours=6)
# yesterday = datetime.date.today() - datetime.timedelta(days=1)

start = datetime.datetime.combine(yesterday, datetime.time(0, 0)).replace(tzinfo=pytz.utc)
end = datetime.datetime.combine(today, datetime.time(0, 0)).replace(tzinfo=pytz.utc)
occupant_records = mycol_sim.find({'ref_id': 'DMC02-CWS', 'timestamp': {'$gte': start}})

occu_dt = []
for c in occupant_records:
    occu_dt.append(c)
print(len(occu_dt))
data = pd.DataFrame(occu_dt)

main_data = data['data']
ahu = []
for i in main_data:
    res = i['AHU_OUTboundary']
    yy.append(res)
print(len(yy))

for t in data['timestamp']:
    print(t)
    xx.append(t)
print(len(xx))


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
        AHU_OUT = sim_main_data['AHU_OUTboundary']
        yy.append(AHU_OUT)

        time = x['timestamp']
        xx.append(time)

st = Thread(target=read_stream, args=())
st.start()
st.is_alive()

@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    ahu=yy
    print(ahu)
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
