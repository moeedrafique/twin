import pathlib

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

myclient = pymongo.MongoClient("mongodb+srv://shahid_123:iRRHpdYoWApzFkWw@trymedriver.nmfto.mongodb.net/trymeTaxiDatabase?retryWrites=true&w=majority")
mydb = myclient["trymeTaxiDatabase"]
mycol_sim = mydb["drivers"]

# tariff_elec = mycol_sim.find()

buildings = mycol_sim.find({'isLive': True})
b_dt = pd.DataFrame.from_dict(buildings)
business = []
for i in b_dt:
    business.append(i)

print(b_dt)
