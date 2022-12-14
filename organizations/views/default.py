# -*- coding: utf-8 -*-
import base64
import codecs
from statistics import mean

import gridfs
import numpy as np
import pandas as pd
import pymongo
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
import plotly.graph_objs as go
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from sweetify import sweetify

from allauth.account.models import UserProfile
from organizations.forms import joinForm
from organizations.models import Organization
from organizations.views.base import ViewFactory
from organizations.views.mixins import AdminRequiredMixin
from organizations.views.mixins import MembershipRequiredMixin
from organizations.views.mixins import OwnerRequiredMixin

bases = ViewFactory(Organization)


def OrganizationView(request, organization_pk):
    organization = get_object_or_404(Organization, id=organization_pk)
    context = {'organization': organization}
    return render(request, 'organizations/organization_view.html', context)


def join(request):
    if request.method == 'POST':
        form = joinForm(request.POST)
        if request.method == 'POST':
            form = joinForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                template = render_to_string('main_app/email_template.html', {'name': name})

                email = EmailMessage(
                    'Thank you for your interest.',
                    template,
                    settings.EMAIL_HOST_USER,
                    [email],
                )

                email.fail_silently = False
                email.content_subtype = 'html'
                email.send()
                form.save()
                messages.success(request, 'Business Customer Added successfully!')
                return redirect('organization_list')
            else:
                messages.error(request, 'Something Went Wrong! Carefully Check Configuration Setting...')
    else:

        form = joinForm()
    context = {'form': form}
    return render(request, 'join.html', context)


@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login'), name='dispatch')
class OrganizationList(bases.OrganizationList):
    pass


class OrganizationCreate(bases.OrganizationCreate):
    """
    Allows any user to create a new organization.
    """

    pass


class OrganizationDetail(MembershipRequiredMixin, bases.OrganizationDetail):
    pass


class OrganizationUpdate(AdminRequiredMixin, bases.OrganizationUpdate):
    pass


class OrganizationDelete(OwnerRequiredMixin, bases.OrganizationDelete):
    pass


class OrganizationUserList(MembershipRequiredMixin, bases.OrganizationUserList):
    pass


class OrganizationUserDetail(AdminRequiredMixin, bases.OrganizationUserDetail):
    pass


class OrganizationUserUpdate(AdminRequiredMixin, bases.OrganizationUserUpdate):
    pass


class OrganizationUserCreate(AdminRequiredMixin, bases.OrganizationUserCreate):
    pass


class OrganizationUserRemind(AdminRequiredMixin, bases.OrganizationUserRemind):
    pass


class OrganizationUserDelete(AdminRequiredMixin, bases.OrganizationUserDelete):
    pass


myclient = pymongo.MongoClient(
    "mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol = mydb["iiot"]
mycol_sim = mydb["simulation_sensor_locations"]
mycol_occu = mydb["occupants"]
mycol_energy = mydb["energy_building"]
mycol_energy_building = mydb["energy_building"]
mycol_schedule = mydb["schedules"]
mycol_tariff = mydb["tariffs"]


def viewDashboard(request, organization_pk):
    business_detail = get_object_or_404(Organization, id=organization_pk)
    if business_detail.name == "Digital Media Centre":
        query = {
            'business': 'Digital Media Centre',
            'building': 'DMC02',
            'floor': 'ground',
            'room': 'Coworking Space',
            'sensors_of': 'BMS'
        }
        now = timezone.now()
        # all_records = mycol.find({'timestamp': {"$lt": now - timedelta(hours=24)}}).sort('_id',-1).limit(96)
        all_records = mycol.find({'ref_id': 'dmc02'}).sort('_id', -1).limit(96)

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
        blob_filename_obj = mydb.fs.files.find_one(
            {'filename.business': 'Digital Media Centre', 'filename.type': blob_name},
            sort=[('_id', pymongo.DESCENDING)])
        blob_filename_id = blob_filename_obj['_id']
        blob_output_data = fs.get(blob_filename_id).read()
        blob_output = blob_output_data.decode()

        floor_name = "floorplan"
        floor_filename_obj = mydb.fs.files.find_one(
            {'filename.business': 'Digital Media Centre', 'filename.type': floor_name},
            sort=[('_id', pymongo.DESCENDING)])
        floor_filename_id = floor_filename_obj['_id']
        floor_output_data = fs.get(floor_filename_id).read()
        floor_output = floor_output_data.decode()
        # print(floor_output)
        context = {"avg_temp_ahu": avg_temp_ahu, "avg_temp_fcu_3": avg_temp_fcu_3, "avg_temp_fcu_4": avg_temp_fcu_4,
                   "avg_ahu_fr": avg_ahu_fr, "occu_dt": occu_dt, 'blob_output': blob_output,
                   'floor_output': floor_output,
                   "business_detail": business_detail}
        template = 'dmc_page.htm'
    else:
        query = {
            'business': 'Sheffield University',
            'building': 'Diamond',
            'floor': 'third',
            'room': 'WR/03',
            'sensors_of': 'BMS'
        }
        now = timezone.now()
        # all_records = mycol.find({'timestamp': {"$lt": now - timedelta(hours=24)}}).sort('_id',-1).limit(96)
        all_records = mycol.find({'business': 'Sheffield University'}).sort('_id', -1).limit(96)

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

        fcu_09 = []
        for i in main_data:
            res = i['fcu_09'][0]
            fcu_09.append(res)

        avg_temp_fcu_09 = np.mean(fcu_09)

        fcu_10 = []
        for i in main_data:
            res = i['fcu_10'][0]
            fcu_10.append(res)

        avg_temp_fcu_10 = np.mean(fcu_10)

        # FLOW RATE / Comfort
        ahu_fr = []
        for i in main_data:
            res = i['ahu'][1]
            ahu_fr.append(res)

        avg_ahu_fr = np.mean(ahu_fr)

        # sim_rec = mycol_sim.find().sort('_id', -1)
        # sim_dt = []
        # for c in sim_rec:
        #     sim_dt.append(c)
        #
        # sim_data = pd.DataFrame(sim_dt)
        # sim_main_data = sim_data['data'][0]
        # first_inlet_data = sim_main_data['inletsinlet1'] + sim_main_data['inletsinlet2'] + sim_main_data['inletsinlet3']
        # mean_first_inlet = first_inlet_data / 3
        # print(mean_first_inlet)
        # print(sim_main_data)

        # inlet_1 = []
        # for i in sim_main_data:
        #     res = i['inletsinlet1'][0] + i['inletsinlet2'] + i['inletsinlet3'] / 3
        #     inlet_1.append(res)
        # print(inlet_1)

        # sim_timestamp_rec = sim_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # sim_timestamp = []
        # for i in sim_timestamp_rec:
        #     sim_timestamp.append(i)
        # print(sim_timestamp[-1])

        occupant_records = mycol_occu.find({}).limit(1)
        occu_dt = []
        for c in occupant_records:
            occu_dt.append(c)

        fs = gridfs.GridFS(mydb)

        blob_name = "blobs"
        blob_filename_obj = mydb.fs.files.find_one(
            {'filename.business': 'Sheffield University', 'filename.type': blob_name},
            sort=[('_id', pymongo.DESCENDING)])
        blob_filename_id = blob_filename_obj['_id']
        blob_output_data = fs.get(blob_filename_id).read()
        blob_output = blob_output_data.decode()

        floor_name = "floorplan"
        floor_filename_obj = mydb.fs.files.find_one(
            {'filename.business': 'Sheffield University', 'filename.type': floor_name},
            sort=[('_id', pymongo.DESCENDING)])
        floor_filename_id = floor_filename_obj['_id']
        floor_output_data = fs.get(floor_filename_id).read()
        floor_output = floor_output_data.decode()
        # print(floor_output)
        context = {"avg_temp_ahu": avg_temp_ahu, "avg_temp_fcu_09": avg_temp_fcu_09, "avg_temp_fcu_10": avg_temp_fcu_10,
                   "avg_ahu_fr": avg_ahu_fr,
                   "occu_dt": occu_dt, 'blob_output': blob_output, 'floor_output': floor_output}
        template = 'svg.htm'
    return render(request, template, context)


def viewSummary(request, organization_pk):
    business_detail = get_object_or_404(Organization, id=organization_pk)
    query = {
        'business': 'Digital Media Centre',
        'building': 'DMC02',
        'floor': 'ground',
        'room': 'Coworking Space',
        'sensors_of': 'BMS'
    }
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999) - timedelta(days=0)

    previous_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    previous_end = now - timedelta(days=1)
    # all_records = mycol.find({'timestamp': {"$lt": now - timedelta(hours=24)}}).sort('_id',-1).limit(96)
    # all_records = mycol_sim.find({'ref_id': 'DMC02-CWS'}).sort('_id', -1).limit(1)
    today_sim_records = mycol_sim.find({'ref_id': 'DMC02-CWS', 'timestamp': {'$gte': today_start, '$lte':today_end}})
    yesterday_sim_records = mycol_sim.find({'ref_id': 'DMC02-CWS', 'timestamp': {'$gte': previous_start, '$lte':previous_end}})

    today_sim_dt = []
    for c in today_sim_records:
        today_sim_dt.append(c)

    today_sim_data = pd.DataFrame(today_sim_dt)
    #
    today_sim_main_data = today_sim_data['data']
    #
    today_sim_total = []
    for i in today_sim_main_data:
        res = i["sf1_2"] + i["sf2_2"] + i["ahu_out"] + i["eg1_1"] + i[
            "fcu_in"] + i["main_door"] + i['sg1_1'] + i['sg2_2'] + i[
                  'sg3_2'] + \
              i['sg4_2'] + i['sg5_2'] + \
              i['sg6_2']
        today_sim_total.append(res)
    today_avg = mean(today_sim_total)
    # print(today_avg)

    yesterday_sim_dt = []
    for c in yesterday_sim_records:
        yesterday_sim_dt.append(c)

    yesterday_sim_data = pd.DataFrame(yesterday_sim_dt)
    #
    yesterday_sim_main_data = yesterday_sim_data['data']
    #
    yesterday_sim_total = []
    for i in yesterday_sim_main_data:
        res = i["sf1_2"] + i["sf2_2"] + i["ahu_out"] + i["eg1_1"] + i[
            "fcu_in"] + i["main_door"] + i['sg1_1'] + i['sg2_2'] + i[
                  'sg3_2'] + \
              i['sg4_2'] + i['sg5_2'] + \
              i['sg6_2']
        yesterday_sim_total.append(res)
    yesterday_avg = mean(yesterday_sim_total)
    # print(yesterday_avg)

    subtract_temp = (yesterday_avg - today_avg)
    divide_temp = (subtract_temp / yesterday_avg) * 100
    change_in_temp = "{:.2f}".format(divide_temp).replace("-", "")
    if divide_temp > 0:
        temp_class_name = "feather icon-arrow-up m-r-15"
    else:
        temp_class_name = "feather icon-arrow-down m-r-15"


    datetime_today = now.strftime('%Y-%m-%d')
    calc_yesterday = now - timedelta(days=1)
    datetime_yesterday = calc_yesterday.strftime('%Y-%m-%d')
    today_energy_records = mycol_energy.find({'ref_id': 'DMC02_Energy', 'datetime': datetime_today})
    yesterday_energy_records = mycol_energy.find({'ref_id': 'DMC02_Energy', 'datetime': datetime_yesterday})
    energy_dt = []
    for c in today_energy_records:
        energy_dt.append(c)

    ener_data = pd.DataFrame(energy_dt)
    #
    en_main_data = ener_data['data']
    #
    today_total = []
    for i in en_main_data:
        res = i['electricity'] + i['gas']
        today_total.append(res)
    today_sum = sum(today_total)
    # print(today_sum)

    yesterdy_energy_dt = []
    for c in yesterday_energy_records:
        yesterdy_energy_dt.append(c)

    yesterday_ener_data = pd.DataFrame(yesterdy_energy_dt)
    #
    yesterday_en_main_data = yesterday_ener_data['data']
    #
    yesterday_today_total = []
    for i in yesterday_en_main_data:
        res = i['electricity'] + i['gas']
        yesterday_today_total.append(res)
    yesterday_sum = sum(yesterday_today_total)
    # print(yesterday_sum)

    subtract_energies = (yesterday_sum - today_sum)
    divide_energy = (subtract_energies / yesterday_sum) * 100
    change_in_energy = "{:.2f}".format(divide_energy).replace("-", "")
    # print(change_in_energy)
    if divide_energy > 0:
        energy_class_name = "feather icon-arrow-up m-r-15"
    else:
        energy_class_name = "feather icon-arrow-down m-r-15"
    #
    elec = []
    for i in en_main_data:
        res = i['electricity']
        elec.append(res)

    # total_energy = [x + y for x, y in zip(gas, elec)]
    # print(total_energy)
    # print(len(energy_dt))

    fs = gridfs.GridFS(mydb)

    blob_name = "boxes"
    blob_filename_obj = mydb.fs.files.find_one(
        {'filename.business': 'Digital Media Centre', 'filename.type': blob_name}, sort=[('_id', pymongo.DESCENDING)])
    blob_filename_id = blob_filename_obj['_id']
    blob_output_data = fs.get(blob_filename_id).read()
    # blob_output = blob_output_data.decode()
    location = '/home/moeedrafique/twin/static/img/'
    outputFile = codecs.open(location + f"{blob_name}.jpeg", "wb")
    outputFile.write(blob_output_data)
    outputFile.close()

    floor_name = "floorplan"
    floor_filename_obj = mydb.fs.files.find_one(
        {'filename.business': 'Digital Media Centre', 'filename.type': floor_name}, sort=[('_id', pymongo.DESCENDING)])
    floor_filename_id = floor_filename_obj['_id']
    floor_output_data = fs.get(floor_filename_id).read()
    # floor_output = floor_output_data.decode()
    outputFile1 = codecs.open(location + f"{floor_name}.jpeg", "wb")
    outputFile1.write(floor_output_data)
    outputFile1.close()

    context = {"energy_dt": energy_dt,
               'energy_class_name': energy_class_name,
               "change_in_temp": change_in_temp, "change_in_energy": change_in_energy,
               'temp_class_name': temp_class_name}
    template = 'summary.html'
    return render(request, template, context)

def energyDash(request, organization_pk):
    business_detail = get_object_or_404(Organization, id=organization_pk)
    now = timezone.now()
    current_month = datetime.now().month
    month_start = datetime.today().replace(day=1)
    month_start_strft = month_start.strftime('%Y-%m-%d')
    current_month_strft = month_start.strftime('%B')
    print(month_start)
    current_date = datetime.today()
    current_date_strft = current_date.strftime('%Y-%m-%d')
    print(current_date)

    diff = current_date - month_start
    actual_diff = diff.days + 1

    tariff_elec = mycol_tariff.find_one({'business':'Digital Media Centre', 'energy_type':'electricity'}, sort=[( '_id', pymongo.DESCENDING )])
    tariff_gas = mycol_tariff.find_one({'business':'Digital Media Centre', 'energy_type':'gas'}, sort=[( '_id', pymongo.DESCENDING )])
    # print(tariff['anytime'])
    energy_building = mycol_energy_building.find({'business':'Digital Media Centre', 'datetime': {'$gte': month_start_strft, '$lte': '2022-12-31'}})

    ener_data = pd.DataFrame(energy_building)
    # print(ener_data.count())
    #
    en_main_data = ener_data['data']
    time_main_data = ener_data['datetime']
    print(time_main_data)
    time_dt = []
    for i in time_main_data:
        time_dt.append(i)

    energy_dt = []
    for i in en_main_data:
        res = i['electricity']
        energy_dt.append(res)
    elec_sum = sum(energy_dt)
    print("EDT", energy_dt)
    # print(tariff_elec['anytime'])
    tariff_cost_elec = elec_sum * tariff_elec['anytime'] / 100
    print("Tarriffs Cost", tariff_cost_elec)
    standing_charge_elec = actual_diff * tariff_elec['standing_cnarge'] / 100
    print(standing_charge_elec)

    cost_elec = tariff_cost_elec + standing_charge_elec
    print(cost_elec)

    gas_dt = []
    for i in en_main_data:
        res = i['gas']
        gas_dt.append(res)
    gas_sum = sum(gas_dt)
    # print(gas_sum)

    tariff_cost_gas = gas_sum * tariff_gas['anytime'] / 100
    standing_charge_gas =  actual_diff * tariff_gas['standing_cnarge'] / 100
    cost_gas = tariff_cost_gas + standing_charge_gas
    print(cost_gas)

    total_cost = cost_elec + cost_gas
    print("Total Cost is:", total_cost)


    # CHANGE IN COST
    current_month = datetime.now().month
    month_start = datetime.today().replace(day=1)

    first = now.replace(day=1)
    first_month = first - timedelta(days=31)
    first_month_strft = first_month.strftime('%Y-%m-%d')
    last_month = first - timedelta(days=1)
    last_month_strft = last_month.strftime('%Y-%m-%d')
    last_month_var = last_month.strftime("%B")
    print("Last Month First Day", first_month)
    print("Last Month Last Day", last_month)
    energy_building_lm = mycol_energy_building.find({'business':'Digital Media Centre', 'datetime': {'$gte': first_month_strft, '$lte': last_month_strft}})
    ener_data_lm = pd.DataFrame(energy_building_lm)
    en_main_data_lm = ener_data_lm['data']


    energy_dt_lm = []
    for i in en_main_data_lm:
        res = i['electricity']
        energy_dt_lm.append(res)
    elec_sum_lm = sum(energy_dt_lm)
    print("Last Month ELEC Sum", elec_sum_lm)

    tariff_cost_elec_lm = elec_sum_lm * tariff_elec['anytime'] / 100
    print("Tarriffs Cost Last Month", tariff_cost_elec_lm)
    standing_charge_elec_lm = 31 * tariff_elec['standing_cnarge'] / 100
    print(standing_charge_elec_lm)

    cost_elec_lm = tariff_cost_elec_lm + standing_charge_elec_lm
    print(cost_elec_lm)


    energy_gas_dt_lm = []
    for i in en_main_data_lm:
        res = i['gas']
        energy_gas_dt_lm.append(res)
    gas_sum_lm = sum(energy_gas_dt_lm)
    print("Last Month GAS Sum", gas_sum_lm)

    tariff_cost_gas_lm = gas_sum_lm * tariff_gas['anytime'] / 100
    print("Tarriffs Cost Last Month", tariff_cost_gas_lm)
    standing_charge_gas_lm = 31 * tariff_gas['standing_cnarge'] / 100
    print(standing_charge_gas_lm)

    cost_gas_lm = tariff_cost_gas_lm + standing_charge_gas_lm
    print(cost_gas_lm)

    total_cost_cic_lm = cost_elec_lm + cost_gas_lm
    print("Total Cost Last Month:", total_cost_cic_lm)

    energy_building_cm = mycol_energy_building.find({'business':'Digital Media Centre', 'datetime': {'$gte': month_start_strft, '$lte': '2022-12-31'}})
    ener_data_cm = pd.DataFrame(energy_building_cm)
    en_main_data_cm = ener_data_cm['data']

    first = now.replace(day=1)
    c_month = first - timedelta(days=31)
    c_strft = first_month.strftime('%Y-%m-%d')
    last_month = first - timedelta(days=1)
    last_month_strft = last_month.strftime('%Y-%m-%d')

    energy_dt_cm = []
    for i in en_main_data_cm:
        res = i['electricity']
        energy_dt_cm.append(res)
    elec_sum_cm = sum(energy_dt_cm)
    print("Current Month ELEC Sum", elec_sum_cm)

    energy_gas_dt_cm = []
    for i in en_main_data_cm:
        res = i['gas']
        energy_gas_dt_cm.append(res)
    gas_sum_cm = sum(energy_gas_dt_cm)
    print("Current Month GAS Sum", gas_sum_cm)


    tariff_cost_elec_cm = elec_sum_cm * tariff_elec['anytime'] / 100
    print("", tariff_cost_elec_cm)
    standing_charge_elec_cm = 31 * tariff_elec['standing_cnarge'] / 100
    print(standing_charge_elec_cm)

    cost_elec_cm = tariff_cost_elec_cm + standing_charge_elec_cm
    print("Cost Elec Current Month", cost_elec_cm)

    tariff_cost_gas_cm = gas_sum_cm * tariff_gas['anytime'] / 100
    # print("Tarriffs Cost Gas Current Month", tariff_cost_gas_cm)
    standing_charge_gas_cm = 31 * tariff_gas['standing_cnarge'] / 100
    print(standing_charge_gas_cm)

    cost_gas_cm = tariff_cost_gas_cm + standing_charge_gas_cm
    print("Cost Gas Current Month", cost_gas_cm)

    total_cost_cic = cost_elec_cm + cost_gas_cm
    print("Total Cost is:", total_cost_cic)
    # any_time_cost = tariff.anytime

    total_energy_usuage = energy_dt + gas_dt
    print(total_energy_usuage)
    context = {'business_detail': business_detail, 'cost_elec':cost_elec, 'cost_gas':cost_gas, 'total_cost':total_cost,
               'total_cost_cic_lm':total_cost_cic_lm, 'total_cost_cic':total_cost_cic, 'last_month_var':last_month_var,
               'current_month_strft':current_month_strft, 'total_energy_usuage':total_energy_usuage, 'time_dt':time_dt}
    return render(request, 'energy.htm', context)

def energyDetail(request, organization_pk):
    business_detail = get_object_or_404(Organization, id=organization_pk)
    context = {'business_detail': business_detail}
    return render(request, 'energy_detail.htm', context)

def AirTerminals(request, organization_pk):
    business_detail = get_object_or_404(Organization, id=organization_pk)
    main_data = mycol_sim.find_one({'business':'Digital Media Centre'}, sort=[( '_id', pymongo.DESCENDING )])

    context = {'business_detail': business_detail, 'i':main_data}
    return render(request, 'air_terminals.html', context)

def FlowDistribution(request, organization_pk):
    business_detail = get_object_or_404(Organization, id=organization_pk)

    occupant_records = mycol_occu.find({}).limit(1)
    occu_dt = []
    for c in occupant_records:
        occu_dt.append(c)

    fs = gridfs.GridFS(mydb)

    blob_name = "boxes"
    blob_filename_obj = mydb.fs.files.find_one(
        {'filename.business': 'Digital Media Centre', 'filename.type': blob_name}, sort=[('_id', pymongo.DESCENDING)])
    blob_filename_id = blob_filename_obj['_id']
    blob_output_data = fs.get(blob_filename_id).read()
    # blob_output = blob_output_data.decode()
    location = '/home/moeedrafique/twin/static/img/'
    outputFile = codecs.open(location + f"{blob_name}.jpeg", "wb")
    outputFile.write(blob_output_data)
    outputFile.close()

    floor_name = "floorplan"
    floor_filename_obj = mydb.fs.files.find_one(
        {'filename.business': 'Digital Media Centre', 'filename.type': floor_name}, sort=[('_id', pymongo.DESCENDING)])
    floor_filename_id = floor_filename_obj['_id']
    floor_output_data = fs.get(floor_filename_id).read()
    # floor_output = floor_output_data.decode()
    outputFile1 = codecs.open(location + f"{floor_name}.jpeg", "wb")
    outputFile1.write(floor_output_data)
    outputFile1.close()

    context = {'business_detail': business_detail}
    return render(request, 'local_flow.html', context)


def Scheduling(request, organization_pk):
    business_detail = get_object_or_404(Organization, id=organization_pk)
    if request.method == 'POST':
        schedule_data = {}
        print(request.POST.get('count'))
        for i in range(2):  #####schedule data range is your ui info
            i = i + 1
            schedule_data.update({
                f"Schedule Data Range {i}": {
                    "time_range": {
                        "start_time": request.POST.get(f"timestart{i}"),
                        "end_time": request.POST.get(f"timeend{i}")
                    },
                    "temperature": request.POST.get(f"set_point{i}")
                },
            })

        range_data = {}
        range_data.update({
        "range_start": request.POST.get("range-start"),
        "range_end": request.POST.get("range-end"),
        })
        emp_rec1 = {
        "ref_id": "DMC02-CWS_SD001",
        "user_id": f"{request.user.id}/{request.user.username}",
        "status": "enabled",
        "timestamp": "",
        "post_time": "",
        "business": "",
        "building": "",
        "floor": "",
        "room": "",
        "data_of": "",
        "schedule_type": "",
        "name": request.POST.get("schedule_day_name"),
        "date_range": range_data,
        "days": [request.POST.get("daysOfWeekDisabled")],
        "season": request.POST.get("season"),
        "color": request.POST.get("color"),
        "schedule_data": schedule_data
    }
        rec_id1 = mycol_schedule.insert_one(emp_rec1)
    context = {'business_detail': business_detail}
    return render(request, 'scheduling.html', context)

def SchedulingList(request, organization_pk):
    business_detail = get_object_or_404(Organization, id=organization_pk)
    main_data = mycol_schedule.find()

    if request.method == 'POST':
        print(request.POST.get('ref_id'))
    context = {'business_detail': business_detail, 'main_data':main_data}
    return render(request, 'scheduling_list.html', context)

def SchedulingDetail(request, organization_pk):
    print(request.POST.get('ref_id'))
    business_detail = get_object_or_404(Organization, id=organization_pk)
    schedule = mycol_schedule.find_one(
        {'ref_id': request.POST.get('ref_id')},
        sort=[('_id', pymongo.DESCENDING)])
    context = {'schedule':schedule, 'business_detail': business_detail}
    return render(request, 'scheduling_detail.html', context)

def Tariffs(request, organization_pk):
    business_detail = get_object_or_404(Organization, id=organization_pk)
    tariff_elec = mycol_tariff.find_one({'business':'Digital Media Centre', 'energy_type':'electricity'}, sort=[( '_id', pymongo.DESCENDING )])
    tariff_gas = mycol_tariff.find_one({'business':'Digital Media Centre', 'energy_type':'gas'}, sort=[( '_id', pymongo.DESCENDING )])
    if request.method == 'POST':
        mylist = [
            {"ref_id": "DMC02-T1", "user_id": f"{request.user.id}/{request.user.username}", "timestamp": datetime.now(), "business": "Digital Media Centre", "building": "DMC02", "data_of": "tariffs", "energy_type": "electricity", "energy_company_name": request.POST.get('energy_company_name1'), "other": request.POST.get('other1'), "meter point_admin_no": request.POST.get('mpan1'), "product_name": request.POST.get('product_name1'), "product_type": request.POST.get('product_type1'), "product_end_date": request.POST.get('product_end_date1'), "vat": request.POST.get('vat1'), "anytime": request.POST.get('any_time_elec'), "standing_cnarge": request.POST.get('standing_charges_elec')},
            {"ref_id": "DMC02-T1", "user_id": f"{request.user.id}/{request.user.username}", "timestamp": datetime.now(), "business": "Digital Media Centre", "building": "DMC02", "data_of": "tariffs", "energy_type": "gas", "energy_company_name": request.POST.get('energy_company_name2'), "other": request.POST.get('other2'), "meter point_admin_no": request.POST.get('mpan2'), "product_name": request.POST.get('product_name2'), "product_type": request.POST.get('product_type2'), "product_end_date": request.POST.get('product_end_date2'), "vat": request.POST.get('vat2'), "anytime": request.POST.get('any_time_gas'), "standing_cnarge": request.POST.get('standing_charges_gas')},

        ]
        rec_id1 = mycol_tariff.insert_many(mylist)
    context = {'business_detail':business_detail, 'tariff_elec':tariff_elec, 'tariff_gas':tariff_gas}
    return render(request, 'tariffs.html', context)

def underConstruction(request):
    return render(request, 'under_conc.html')

@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/login'), name='dispatch')
class StaffUserUpdateView(SuccessMessageMixin, UpdateView):
    template_name = "organizations/update-employee.htm"
    model = User
    fields = ["first_name", "last_name", "email", "username", "is_active"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staffuser = UserProfile.objects.get(auth_user_id=self.object.pk)
        context["staffuser"] = staffuser
        return context

    def form_valid(self, form):
        # Saving Custom User Object for Merchant User
        user = form.save(commit=False)
        user.save()

        # Saving Merchant user
        staffuser = UserProfile.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic", False):
            profile_pic = self.request.FILES["profile_pic"]
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            staffuser.profile_pic = profile_pic_url
            staffuser.dob = self.request.POST.get("dob")
            staffuser.id_card_no = self.request.POST.get("id_card_no")
            staffuser.nationality = self.request.POST.get("nationality")
            staffuser.city = self.request.POST.get("city")
            staffuser.postal_code = self.request.POST.get("postal_code")
            staffuser.house_address = self.request.POST.get("house_address")
            staffuser.phone_number = self.request.POST.get("phone_number")
            staffuser.landline = self.request.POST.get("landline")
            staffuser.emergency_contact = self.request.POST.get("emergency_contact")
            staffuser.medical_history = self.request.POST.get("medical_history")

        staffuser.save()
        sweetify.success(self.request, 'Staff User Updated Successfully', icon="success", timer=30000)
        return HttpResponseRedirect(reverse("join"))
