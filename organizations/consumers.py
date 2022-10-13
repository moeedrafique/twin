
import json
from datetime import datetime, timedelta
from random import randint
from statistics import mean
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
mycol_energy_data = mydb["energy_data"]



class GraphConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        def read_stream():
            now = timezone.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=0)
            today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=0)

            previous_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            previous_end = now - timedelta(days=1)

            today_sim_records = mycol_sim.find(
                {'ref_id': 'DMC02-CWS', 'timestamp': {'$gte': today_start, '$lte': today_end}})
            yesterday_sim_records = mycol_sim.find(
                {'ref_id': 'DMC02-CWS', 'timestamp': {'$gte': previous_start, "$lte": previous_end}})

            today_sim_dt = []
            for c in today_sim_records:
                today_sim_dt.append(c)

            today_sim_data = pd.DataFrame(today_sim_dt)
            #
            today_sim_main_data = today_sim_data['data']
            #
            today_sim_total = []
            for i in today_sim_main_data:
                res = i["SF1_2boundary"] + i["SF2_2boundary"] + i["AHU_OUTboundary"] + i["EG1_1boundary"] + i[
                    "FCU_INboundary"] + i["MAIN_DOORboundary"] + i['SG1_1boundary'] + i['SG2_2boundary'] + i[
                          'SG3_2boundary'] + \
                      i['SG4_2boundary'] + i['SG5_2boundary'] + \
                      i['SG6_2boundary']
                today_sim_total.append(res)
            today_avg = mean(today_sim_total)
            print(today_avg)

            yesterday_sim_dt = []
            for c in yesterday_sim_records:
                yesterday_sim_dt.append(c)

            yesterday_sim_data = pd.DataFrame(yesterday_sim_dt)
            #
            yesterday_sim_main_data = yesterday_sim_data['data']
            #
            yesterday_sim_total = []
            for i in yesterday_sim_main_data:
                res = i["SF1_2boundary"] + i["SF2_2boundary"] + i["AHU_OUTboundary"] + i["EG1_1boundary"] + i[
                    "FCU_INboundary"] + i["MAIN_DOORboundary"] + i['SG1_1boundary'] + i['SG2_2boundary'] + i[
                          'SG3_2boundary'] + \
                      i['SG4_2boundary'] + i['SG5_2boundary'] + \
                      i['SG6_2boundary']
                yesterday_sim_total.append(res)
            yesterday_avg = mean(yesterday_sim_total)
            print(yesterday_avg)

            subtract_temp = (yesterday_avg - today_avg)
            divide_temp = (subtract_temp / yesterday_avg) * 100
            change_in_temp = divide_temp
            print(change_in_temp)

            for change in mycol_sim.watch([{
                '$match': {
                    'operationType': {'$in': ['replace', 'insert']},
                    'fullDocument.business': 'Digital Media Centre',
                }}]):

                O1T0 = change["fullDocument"]["data"]["AHU_OUTboundary"]
                O1T1 = change["fullDocument"]["data"]["EG1_1boundary"]
                O2T1 = change["fullDocument"]["data"]["FCU_INboundary"]
                O3T1 = change["fullDocument"]["data"]["MAIN_DOORboundary"]
                O4T1 = change["fullDocument"]["data"]["SF1_2boundary"]
                O5T1 = change["fullDocument"]["data"]["SF2_2boundary"]
                O6T1 = change["fullDocument"]["data"]["SG1_1boundary"]
                O7T1 = change["fullDocument"]["data"]["SG2_2boundary"]
                O8T1 = change["fullDocument"]["data"]["SG3_2boundary"]
                O1T2 = change["fullDocument"]["data"]["SG4_2boundary"]
                O2T2 = change["fullDocument"]["data"]["SG5_2boundary"]
                O3T2 = change["fullDocument"]["data"]["SG6_2boundary"]

                data = [O1T0, O1T1, O2T1, O3T1, O4T1, O5T1, O6T1, O7T1, O8T1, O1T2, O2T2, O3T2]

                sum_all = O1T0 + O1T1 + O2T1 + O3T1 + O4T1 + O5T1 + O6T1 + O7T1 + O8T1 + O1T2 + O2T2 + O3T2
                print(f'Sum is {sum_all}')
                today_sim_total.append(sum_all)
                avg = float("{:.2f}".format(change_in_temp))
                if avg > 0:
                    class_name = "feather icon-arrow-up"
                else:
                    class_name = "feather icon-arrow-down"

                self.send(json.dumps({'value': data, 'avg':avg, 'class_name':class_name}))
            # for change in mycol_energy_data.watch([{
            #     '$match': {
            #         'operationType': {'$in': ['replace', 'insert']},
            #         'fullDocument.business': 'Digital Media Centre',
            #     }}]):
            #     O1T0 = change["fullDocument"]["data"]["AHU_OUTboundary"]
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


class GraphConsumer3(WebsocketConsumer):
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