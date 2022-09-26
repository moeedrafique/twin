# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path

from organizations.views import default as views
# from organizations.dash_apps import example
# from organizations.dash_apps import inletsinlet2
# from organizations.dash_apps import outlet
# app_name = "organizations"

urlpatterns = [
    path('join/', views.join, name='join'),
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
                path('dashboard/', views.viewDashboard,
                     name='dashboard'
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
