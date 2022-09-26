from django.urls import path

from .consumers import *

ws_urlpatterns = [
    path('ws/graph/', GraphConsumer.as_asgi()),
    path('ws/graph1/', GraphConsumer1.as_asgi()),
    path('ws/graph2/', GraphConsumer2.as_asgi()),
]