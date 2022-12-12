# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path

from organizations.views import default as views
from organizations.dash_apps import gauge
from organizations.dash_apps import pie
from organizations.dash_apps import energy_usuage
from organizations.dash_apps import electric
from organizations.dash_apps import gas
from organizations.dash_apps import hvac
from organizations.dash_apps import temp_vent_data
from organizations.dash_apps import update_db
from organizations.dash_apps import AHU_OUTboundary
# from organizations.dash_apps import SG_boundary
# from organizations.dash_apps import SF_boundary
# app_name = "organizations"

urlpatterns = [
    path('join/', views.join, name='join'),
    path('under-construction/', views.underConstruction, name='under_conc'),
    path('staff-update/<slug:pk>/', views.StaffUserUpdateView.as_view(), name="staff_update"),
    path(
        "",
        view=login_required(views.OrganizationList.as_view()),
        name="organization_list",
    ),
    path(
        "add/",
        view=login_required(views.OrganizationCreate.as_view()),
        name="organization_add",
    ),
    path(
        "<int:organization_pk>/",
        include(
            [
                path('summary/', views.viewSummary,
                     name='summary'
                     ),
                path('air-terminals/', views.AirTerminals,
                     name='air_terminals'
                     ),
                path('localised_flow_distribution/', views.FlowDistribution,
                     name='flow_distribution'
                     ),
                path('energy-dashboard/', views.energyDash,
                     name='energy'
                     ),
                path('energy-usage/', views.energyDetail,
                     name='energy-detail'
                     ),
                path('scheduling/', views.Scheduling,
                     name='scheduling'
                     ),
                path('scheduling-detail/', views.SchedulingDetail,
                     name='scheduling_detail'
                     ),
                path('scheduling-list/', views.SchedulingList,
                     name='scheduling_list'
                ),
                path('tariffs/', views.Tariffs,
                     name='tariffs'
                     ),
                path(
                    "",
                    view=login_required(views.OrganizationDetail.as_view()),
                    name="organization_detail",
                ),
                path(
                    "view/",
                    view=login_required(views.OrganizationView),
                    name="organization_view",
                ),
                path(
                    "edit/",
                    view=login_required(views.OrganizationUpdate.as_view()),
                    name="organization_edit",
                ),
                path(
                    "delete/",
                    view=login_required(views.OrganizationDelete.as_view()),
                    name="organization_delete",
                ),
                path(
                    "people/",
                    include(
                        [
                            path(
                                "",
                                view=login_required(
                                    views.OrganizationUserList.as_view()
                                ),
                                name="organization_user_list",
                            ),
                            path(
                                "add/",
                                view=login_required(
                                    views.OrganizationUserCreate.as_view()
                                ),
                                name="organization_user_add",
                            ),
                            path(
                                "<int:user_pk>/remind/",
                                view=login_required(
                                    views.OrganizationUserRemind.as_view()
                                ),
                                name="organization_user_remind",
                            ),
                            path(
                                "<int:user_pk>/",
                                view=login_required(
                                    views.OrganizationUserDetail.as_view()
                                ),
                                name="organization_user_detail",
                            ),
                            path(
                                "<int:user_pk>/edit/",
                                view=login_required(
                                    views.OrganizationUserUpdate.as_view()
                                ),
                                name="organization_user_edit",
                            ),
                            path(
                                "<int:user_pk>/delete/",
                                view=login_required(
                                    views.OrganizationUserDelete.as_view()
                                ),
                                name="organization_user_delete",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
