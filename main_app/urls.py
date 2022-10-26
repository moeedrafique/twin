from django.urls import path
from . import views
# from main_app.dash_apps import example
# from main_app.dash_apps import inletsinlet2
# from main_app.dash_apps import outlet
urlpatterns = [
    path('', views.home, name='home'),
    path('summary/', views.Summary, name='summary'),
    # path('<slug:slug>/local/', views.viewDashboard, name='local'),
    # path('energy/', views.energyDash, name='energy'),
    # path('energy-usage/', views.energyDetail, name='energy-detail'),
    # path('business/<slug:slug>/', views.business, name='business'),
    # path('invite/', views.invite, name='invite'),
    # path('accounts/signup/', views.register, name='register'),
    # path('all-records/', views.allRecords, name='all_records'),
    path('account-setup/', views.accountsSetup, name='account-setup'),
    # path('<slug:slug>/', views.viewDashboard, name='view-dashboard'),
    # path('svg/', views.svgPage, name='svg'),
    # path('dmc/', views.dmcPage, name = 'dmc'),
    # path("send_otp", views.send_otp,name="send otp"),
    # path("send_mail", views.sendEmail,name="send_mail"),
    # path("add-user", AccountUserAddForm(),name=""),
    ]
