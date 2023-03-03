import dash_extendable_graph as deg
import dash
import pymongo
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime, timedelta
from django.utils import timezone
from threading import Thread
import random
import pandas as pd


app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol_sim = mydb["simulation_sensor_locations"]

app = dash.Dash('temp_vent_data')

xx = []
yy = []


now = datetime.now()
today_start = now.replace(hour=8, minute=0, second=0, microsecond=0) - timedelta(days=0)
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
        print(time)
        xx.append(time)

st = Thread(target=read_stream, args=())
st.start()
st.is_alive()

app.layout = html.Div([
    deg.ExtendableGraph(
        id='extendablegraph_example',
        figure=dict(
            data=[{'x': [xx],
                   'y': [yy],
                   'mode':'lines+markers'
                   }],
        )
    ),
    dcc.Interval(
        id='interval_extendablegraph_update',
        interval=1000,
        n_intervals=0,
        max_intervals=-1),
    html.Div(id='output')
])


@app.callback(Output('extendablegraph_example', 'extendData'),
              [Input('interval_extendablegraph_update', 'n_intervals')],
              [State('extendablegraph_example', 'figure')])

def update_graph_scatter(n_intervals, existing):
    x_new = existing['data'][0]['x'][-1]
    print(existing['data'][0]['y'])
    y_new = existing['data'][0]['y'][-1]
    return [dict(x=[x_new], y=[y_new])]

    # return {'data': [data], 'layout':layout}


if __name__ == '__main__':
    app.run_server(debug=True)