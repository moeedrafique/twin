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
#
# app = dash.Dash()
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
#
# labels = ["Electricity", "Gas"]
# values = [4500, 2500, 1053, 500]
# # Create subplots: use 'domain' type for Pie subplot
# fig = go.Figure(data=[go.Pie(labels=labels, values=[16, 15], hole=.3)])
#
# # Use `hole` to create a donut-like pie chart
# fig.update_traces(hole=.4, hoverinfo="label+percent")
#
# fig.update_layout(
#     title_text="Global Emissions 1990-2011",
#     # Add annotations in the center of the donut pies.
#     annotations=[dict(text='GHG', x=0.18, y=0.5, font_size=20, showarrow=False)])
# fig.show()
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
