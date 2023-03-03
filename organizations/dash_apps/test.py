import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from pymongo import MongoClient

# Create a Dash application
app = dash.Dash(__name__)

# Create the layout
app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

# Create the MongoDB client and database
client = MongoClient('mongodb+srv://twidy_dashboard:9TInnovations@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority')
db = client['twin_dynamics']
collection = db['simulation_sensor_locations']

# Create the initial data
occupant_records = collection.find({}).sort('_id',-1).limit(300)

occu_dt = []
for c in occupant_records:
    occu_dt.append(c)
# print(len(occu_dt))
data = pd.DataFrame(occu_dt)
main_data = data['data']

MAIN_DOOR = []
xx = []

for i in main_data:
    res = i['main_door']
    MAIN_DOOR.append(res)

for t in data['timestamp']:
    # print(t)
    xx.append(t)

x = [xx]
y = [MAIN_DOOR]

print(x)

# Create the initial trace
trace = go.Scatter(x=x, y=y, mode='markers')

# Create the initial layout
layout = go.Layout(title='Real-Time Plotly Dash Graph', xaxis={'title': 'X Axis'}, yaxis={'title': 'Y Axis'})

# Combine the trace and layout to create the initial figure
figure = go.Figure(data=[trace], layout=layout)

# Create the initial graph
@app.callback(Output('graph', 'figure'), [Input('interval', 'n_intervals')])
def update_graph(n_intervals):
    return figure

# Fetch the latest data from MongoDB
def get_data():
    data = collection.find_one(sort=[('timestamp', -1)])
    return data

# def update_data(n_intervals):
#     data = get_data()
#     x.append(data['timestamp'])
#     y.append(data['main_door'])
#     figure['data'][0]['x'] = x
#     figure['data'][0]['y'] = y
#     return figure



if __name__ == '__main__':
    app.run_server(debug=True)