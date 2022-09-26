import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from bson import ObjectId
from django.contrib.auth import authenticate, get_user_model

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from organizations.backends import invitation_backend
from organizations.forms import OrganizationUserAddForm, OrganizationAddForm
from organizations.models import Organization
from organizations.abstract import AbstractOrganization
from plotly.offline import plot

from .forms import *
# from invitations.forms import InviteForm
from django.contrib import messages
from invitations.utils import get_invitation_model
import sweetify
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
# Create your views here.
import pymongo
from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference
import random
from datetime import datetime, timedelta
import gridfs
import math, random
import svgutils.compose as sc
from IPython.display import SVG, display, display_svg
# import plotly.express as px

def home(request):
    return render(request, 'home.html')

def accountsSetup(request):
    return render(request, 'account-setup.htm')

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def send_otp(request):
    email = request.POST.get('email')
    print(email)
    o = generateOTP()
    htmlgen = '<p>Your OTP is </p>' + o
    send_mail('OTP request', o, '<your gmail id>', [email], fail_silently=False, html_message=htmlgen)
    return HttpResponse(o)
#
# def join(request):
#     if request.method == 'POST':
#         form = joinForm(request.POST)
#         if request.method == 'POST':
#             form = joinForm(request.POST, request.FILES)
#             if form.is_valid():
#                 name = form.cleaned_data.get('name')
#                 email = form.cleaned_data.get('email')
#                 template = render_to_string('main_app/email_template.html', {'name':name})
#
#                 email = EmailMessage(
#                     'Thank you for your interest.',
#                     template,
#                     settings.EMAIL_HOST_USER,
#                     [email],
#                 )
#
#                 email.fail_silently = False
#                 email.content_subtype = 'html'
#                 email.send()
#                 form.save()
#                 messages.success(request, 'Business Customer Added successfully!')
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Something Went Wrong! Carefully Check Configuration Setting...')
#     else:
#
#         form = joinForm()
#     context = {'form': form}
#     return render(request, 'join.html', context)# def join(request):
#     if request.method == 'POST':
#         form = joinForm(request.POST)
#         if request.method == 'POST':
#             form = joinForm(request.POST, request.FILES)
#             if form.is_valid():
#                 name = form.cleaned_data.get('name')
#                 email = form.cleaned_data.get('email')
#                 template = render_to_string('main_app/email_template.html', {'name':name})
#
#                 email = EmailMessage(
#                     'Thank you for your interest.',
#                     template,
#                     settings.EMAIL_HOST_USER,
#                     [email],
#                 )
#
#                 email.fail_silently = False
#                 email.content_subtype = 'html'
#                 email.send()
#                 form.save()
#                 messages.success(request, 'Business Customer Added successfully!')
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Something Went Wrong! Carefully Check Configuration Setting...')
#     else:
#
#         form = joinForm()
#     context = {'form': form}
#     return render(request, 'join.html', context)


# def business(request, slug):
#     business_detail = get_object_or_404(Business, slug=slug)
#     form = businessForm(instance=business_detail)
#     if request.method == 'POST':
#         form = businessForm(request.POST, request.FILES, instance=business_detail)
#         if form.is_valid():
#             form.save()
#             sweetify.success(request, 'Business Customer Added successfully!', icon="success", timer=30000)
#             # return redirect('home')
#         elif 'email' in request.POST:
#             email = request.POST.get('email')
#             print(email)
#             template = render_to_string('main_app/email_template.html')
#
#             email = EmailMessage(
#                 'PLEASE SIGN UP',
#                 template,
#                 settings.EMAIL_HOST_USER,
#                 [email],
#             )
#
#             email.fail_silently = False
#             email.content_subtype = 'html'
#             email.send()
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#         elif 'status_pass' in request.POST:
#             password = request.POST.get('status_pass')
#             user = authenticate(username=request.user.username, password=password)
#             if user is not None:
#                 if business_detail.status == 'Active':
#                     business_detail.status = 'Deactive'
#                     business_detail.save()
#                     sweetify.success(request, "Business Deactivated Successfully.", icon="success", timer=30000)
#                     return redirect('all_records')
#
#                 elif business_detail.status == 'Deactive':
#                     business_detail.status = 'Active'
#                     business_detail.last_active = datetime.now()
#                     business_detail.save()
#                     sweetify.success(request, "Business Activated Successfully.", icon="success", timer=30000)
#                     return redirect('all_records')
#         else:
#             sweetify.error(request, 'Something Went Wrong! Carefully Check Configuration Setting...', timer=30000)
#
#
#     context = {'form': form, 'business_detail': business_detail}
#     return render(request, 'business.htm', context)

def sendEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        template = render_to_string('main_app/email_template.html')

        email = EmailMessage(
            'PLSESE SIGN UP',
            template,
            settings.EMAIL_HOST_USER,
            [email],
        )

        email.fail_silently = False
        email.content_subtype = 'html'
        email.send()
    context = {}
    return render(request, 'business.htm', context)

def invite(request):
    return render(request, 'main_app/new-user.html')

def register(request):
    if request.method == 'POST':
        form = MyCustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('account_login')
    else:
        form = MyCustomSignupForm()
    return render(request, 'account/signup.html', {'form': form})

# def allRecords(request):
#     all = Business.objects.all()
#     context = {'all': all}
#     return render(request, 'business-customer-list.htm', context)


myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol = mydb["iiot"]
mycol_sim = mydb["simulation_sensor_locations"]
mycol_occu = mydb["occupants"]

def viewDashboard(request, slug):
    business_detail = get_object_or_404(Organization, slug=slug)

    occupant_records = mycol_occu.find({}).limit(1)
    occu_dt = []
    for c in occupant_records:
        occu_dt.append(c)

    fs = gridfs.GridFS(mydb)

    blob_name = "boxes"
    blob_filename_obj = mydb.fs.files.find_one({'filename.business':business_detail.name, 'filename.type': blob_name}, sort=[( '_id', pymongo.DESCENDING )])
    blob_filename_id = blob_filename_obj['_id']
    blob_output_data = fs.get(blob_filename_id).read()
    blob_output = blob_output_data.decode()

    floor_name = "floorplan"
    floor_filename_obj = mydb.fs.files.find_one({'filename.business':business_detail.name, 'filename.type': floor_name}, sort=[( '_id', pymongo.DESCENDING )])
    floor_filename_id = floor_filename_obj['_id']
    floor_output_data = fs.get(floor_filename_id).read()
    floor_output = floor_output_data.decode()
    # print(floor_output)

    context = {'business_detail': business_detail, 'blob_output':blob_output, 'floor_output':floor_output}
    return render(request, 'svg.htm', context)






# FOR FETCHING AND DISPLAYING DASHBOARD DATA
# CHARTS/GRAPHS
def Database(request):

    query = {
        'business': 'Digital Media Centre',
        'building': 'DMC02',
        'floor': 'ground',
        'room': 'Coworking Space',
        'sensors_of': 'BMS'
    }
    now = timezone.now()
    # all_records = mycol.find({'timestamp': {"$lt": now - timedelta(hours=24)}}).sort('_id',-1).limit(96)
    all_records = mycol.find({'ref_id':'dmc02'}).sort('_id',-1).limit(96)

    dt = []
    for c in all_records:
        dt.append(c)

    # print(dt)
    #
    data = pd.DataFrame(dt)
    # print(data)
    main_data = data['data']
    ahu = []
    for i in main_data:
        res = i['ahu'][0]
        ahu.append(res)

    avg_temp_ahu = np.mean(ahu)

    fcu_3 = []
    for i in main_data:
        res = i['fcu_3'][0]
        fcu_3.append(res)

    avg_temp_fcu_3 = np.mean(fcu_3)

    fcu_4 = []
    for i in main_data:
        res = i['fcu_4'][0]
        fcu_4.append(res)

    avg_temp_fcu_4 = np.mean(fcu_4)

    # FLOW RATE / Comfort
    ahu_fr = []
    for i in main_data:
        res = i['ahu'][1]
        ahu_fr.append(res)

    avg_ahu_fr = np.mean(ahu_fr)


    occupant_records = mycol_occu.find({}).limit(1)
    occu_dt = []
    for c in occupant_records:
        occu_dt.append(c)

    fs = gridfs.GridFS(mydb)

    blob_name = "boxes"
    blob_filename_obj = mydb.fs.files.find_one({'filename.business':'Digital Media Centre', 'filename.type': blob_name}, sort=[( '_id', pymongo.DESCENDING )])
    blob_filename_id = blob_filename_obj['_id']
    blob_output_data = fs.get(blob_filename_id).read()
    blob_output = blob_output_data.decode()

    floor_name = "floorplan"
    floor_filename_obj = mydb.fs.files.find_one({'filename.business':'Digital Media Centre', 'filename.type': floor_name}, sort=[( '_id', pymongo.DESCENDING )])
    floor_filename_id = floor_filename_obj['_id']
    floor_output_data = fs.get(floor_filename_id).read()
    floor_output = floor_output_data.decode()
    # print(floor_output)

    context = {"avg_temp_ahu":avg_temp_ahu, "avg_temp_fcu_3":avg_temp_fcu_3, "avg_temp_fcu_4":avg_temp_fcu_4,
               "avg_ahu_fr":avg_ahu_fr,"occu_dt":occu_dt, 'blob_output':blob_output, 'floor_output':floor_output}
    return render(request, 'svg.htm', context)


def dmcPage(request):

    query = {
        'business': 'Sheffield University',
        'building': 'Diamond',
        'floor': 'third',
        'room': 'WR/03',
        'sensors_of': 'BMS'
    }
    now = timezone.now()
    # all_records = mycol.find({'timestamp': {"$lt": now - timedelta(hours=24)}}).sort('_id',-1).limit(96)
    all_records = mycol.find().sort('_id',-1).limit(96)

    dt = []
    for c in all_records:
        dt.append(c)

    # print(dt)
    #
    data = pd.DataFrame(dt)
    # print(data)
    main_data = data['data']
    ahu = []
    for i in main_data:
        res = i['ahu'][0]
        ahu.append(res)

    avg_temp_ahu = np.mean(ahu)

    fcu_3 = []
    for i in main_data:
        res = i['fcu_3'][0]
        fcu_3.append(res)

    avg_temp_fcu_3 = np.mean(fcu_3)

    fcu_4 = []
    for i in main_data:
        res = i['fcu_4'][0]
        fcu_4.append(res)

    avg_temp_fcu_4 = np.mean(fcu_4)

    # FLOW RATE / Comfort
    ahu_fr = []
    for i in main_data:
        res = i['ahu'][1]
        ahu_fr.append(res)

    avg_ahu_fr = np.mean(ahu_fr)

    sim_rec = mycol_sim.find().sort('_id',-1)
    sim_dt = []
    for c in sim_rec:
        sim_dt.append(c)

    sim_data = pd.DataFrame(sim_dt)
    sim_main_data = sim_data['data'][0]
    first_inlet_data = sim_main_data['AHU_OUTboundary'] + sim_main_data['EG1_1boundary'] + sim_main_data[
            'FCU_INboundary']
    mean_first_inlet = first_inlet_data / 3
    print(mean_first_inlet)
    # print(sim_main_data)


    # inlet_1 = []
    # for i in sim_main_data:
    #     res = i['inletsinlet1'][0] + i['inletsinlet2'] + i['inletsinlet3'] / 3
    #     inlet_1.append(res)
    # print(inlet_1)

    sim_timestamp_rec = sim_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

    sim_timestamp = []
    for i in sim_timestamp_rec:
        sim_timestamp.append(i)
    print(sim_timestamp[-1])

    occupant_records = mycol_occu.find({}).limit(1)
    occu_dt = []
    for c in occupant_records:
        occu_dt.append(c)

    fs = gridfs.GridFS(mydb)

    blob_name = "blobs"
    blob_filename_obj = mydb.fs.files.find_one({'filename.type': blob_name}, sort=[( '_id', pymongo.DESCENDING )])
    blob_filename_id = blob_filename_obj['_id']
    blob_output_data = fs.get(blob_filename_id).read()
    blob_output = blob_output_data.decode()

    floor_name = "floorplan"
    floor_filename_obj = mydb.fs.files.find_one({'filename.type': floor_name}, sort=[( '_id', pymongo.DESCENDING )])
    floor_filename_id = floor_filename_obj['_id']
    floor_output_data = fs.get(floor_filename_id).read()
    floor_output = floor_output_data.decode()
    # print(floor_output)

    context = {"avg_temp_ahu":avg_temp_ahu, "avg_temp_fcu_3":avg_temp_fcu_3, "avg_temp_fcu_4":avg_temp_fcu_4,
               "avg_ahu_fr":avg_ahu_fr, 'sim_timestamp':sim_timestamp,
               "occu_dt":occu_dt, 'blob_output':blob_output, 'floor_output':floor_output}
    return render(request, 'dmc_page.htm', context)


def svgPage(request):
    def scatter():
        x1 = [1, 2, 3, 4]
        y1 = [30, 35, 25, 45]

        trace = go.Scatter(
            x=x1,
            y=y1
        )
        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context = {
        'plot1': scatter()
    }
    return render(request, 'svg.htm', context)