# -*- coding: utf-8 -*-
import gridfs
import numpy as np
import pandas as pd
import pymongo
from django.conf import settings
from django.contrib import messages
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
    context = {'organization':organization}
    return render(request, 'organizations/organization_view.html', context)


def join(request):
    if request.method == 'POST':
        form = joinForm(request.POST)
        if request.method == 'POST':
            form = joinForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                template = render_to_string('main_app/email_template.html', {'name':name})

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

myclient = pymongo.MongoClient("mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["twin_dynamics"]
mycol = mydb["iiot"]
mycol_sim = mydb["simulation_sensor_locations"]
mycol_occu = mydb["occupants"]

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
        blob_filename_obj = mydb.fs.files.find_one({'filename.business':'Sheffield University', 'filename.type': blob_name}, sort=[('_id', pymongo.DESCENDING)])
        blob_filename_id = blob_filename_obj['_id']
        blob_output_data = fs.get(blob_filename_id).read()
        blob_output = blob_output_data.decode()

        floor_name = "floorplan"
        floor_filename_obj = mydb.fs.files.find_one({'filename.business':'Sheffield University', 'filename.type': floor_name}, sort=[('_id', pymongo.DESCENDING)])
        floor_filename_id = floor_filename_obj['_id']
        floor_output_data = fs.get(floor_filename_id).read()
        floor_output = floor_output_data.decode()
        # print(floor_output)
        context = {"avg_temp_ahu": avg_temp_ahu, "avg_temp_fcu_09": avg_temp_fcu_09, "avg_temp_fcu_10": avg_temp_fcu_10,
                   "avg_ahu_fr": avg_ahu_fr,
                   "occu_dt": occu_dt, 'blob_output': blob_output, 'floor_output': floor_output}
        template = 'svg.htm'
    return render(request, template, context)


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