
import json
from random import randint
from threading import Thread
from time import sleep
from datetime import datetime, timedelta
from django.utils import timezone
import gridfs
import numpy as np
import pandas as pd
import pymongo
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol = mydb["fs.files"]
mycol_occu = mydb["occupants"]
mycol_sim = mydb["simulation_sensor_locations"]

class GraphConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        def read_stream():
            for change in mycol_occu.watch([{
                '$match': {
                    'operationType': {'$in': ['replace', 'insert']},
                }}]):

                O1T0 = change["fullDocument"]["data"]["o1t0"]
                O1T1 = change["fullDocument"]["data"]["o1t1"]
                O2T1 = change["fullDocument"]["data"]["o2t1"]
                O3T1 = change["fullDocument"]["data"]["o3t1"]
                O4T1 = change["fullDocument"]["data"]["o4t1"]
                O5T1 = change["fullDocument"]["data"]["o5t1"]
                O6T1 = change["fullDocument"]["data"]["o6t1"]
                O7T1 = change["fullDocument"]["data"]["o7t1"]
                O8T1 = change["fullDocument"]["data"]["o8t1"]
                O1T2 = change["fullDocument"]["data"]["o1t2"]
                O2T2 = change["fullDocument"]["data"]["o2t2"]
                O3T2 = change["fullDocument"]["data"]["o3t2"]
                O4T2 = change["fullDocument"]["data"]["o4t2"]
                O5T2 = change["fullDocument"]["data"]["o5t2"]
                O6T2 = change["fullDocument"]["data"]["o6t2"]
                O7T2 = change["fullDocument"]["data"]["o7t2"]
                O8T2 = change["fullDocument"]["data"]["o8t2"]
                O1T3 = change["fullDocument"]["data"]["o1t3"]
                O2T3 = change["fullDocument"]["data"]["o2t3"]
                O3T3 = change["fullDocument"]["data"]["o3t3"]
                O4T3 = change["fullDocument"]["data"]["o4t3"]
                O5T3 = change["fullDocument"]["data"]["o5t3"]
                O6T3 = change["fullDocument"]["data"]["o6t3"]
                O7T3 = change["fullDocument"]["data"]["o7t3"]
                O8T3 = change["fullDocument"]["data"]["o8t3"]
                O1T4 = change["fullDocument"]["data"]["o1t4"]
                O2T4 = change["fullDocument"]["data"]["o2t4"]
                O3T4 = change["fullDocument"]["data"]["o3t4"]
                O4T4 = change["fullDocument"]["data"]["o4t4"]
                O5T4 = change["fullDocument"]["data"]["o5t4"]
                O6T4 = change["fullDocument"]["data"]["o6t4"]
                O7T4 = change["fullDocument"]["data"]["o7t4"]
                O8T4 = change["fullDocument"]["data"]["o8t4"]



                data = [O1T0, O1T1, O2T1, O3T1, O4T1, O5T1, O6T1, O7T1, O8T1, O1T2, O2T2, O3T2, O4T2, O5T2, O6T2, O7T2, O8T2,
                    O1T3, O2T3, O3T3, O4T3, O5T3, O6T3, O7T3, O8T3, O1T4, O2T4, O3T4, O4T4, O5T4, O6T4, O7T4, O8T4]


                self.send(json.dumps({'value': data}))
        st = Thread(target=read_stream, args=())
        st.start()
        st.is_alive()



class GraphConsumer1(WebsocketConsumer):
    def connect(self):
        self.accept()

        def read_stream():
            for change in mycol.watch([{
                '$match': {
                    'operationType': {'$in': ['replace', 'insert']},
                    'fullDocument.filename.business': 'Digital Media Centre',
                    'fullDocument.filename.type': 'boxes'
                }
            }
            ]
            ):
                x = change["fullDocument"]
                fs = gridfs.GridFS(mydb)

                blob_filename_obj = x
                blob_filename_id = blob_filename_obj['_id']
                blob_output_data = fs.get(blob_filename_id).read()
                blob_output = blob_output_data.decode()
                self.send(json.dumps({'blob_output': blob_output}))

        st = Thread(target=read_stream, args=())
        st.start()
        st.is_alive()

class GraphConsumer2(WebsocketConsumer):
    def connect(self):
        self.accept()

        def read_stream():
            for change in mycol.watch([{
                '$match': {
                    'operationType': {'$in': ['replace', 'insert']},
                    'fullDocument.filename.business': 'Digital Media Centre',
                    'fullDocument.filename.type': 'floorplan'
                }
            }
            ]
            ):
                x = change["fullDocument"]
                fs = gridfs.GridFS(mydb)

                floor_filename_obj = x
                floor_filename_id = floor_filename_obj['_id']
                floor_output_data = fs.get(floor_filename_id).read()
                floor_output = floor_output_data.decode()

                self.send(json.dumps({'floor_output': floor_output}))

        st = Thread(target=read_stream, args=())
        st.start()
        st.is_alive()