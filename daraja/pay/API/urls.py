from django.contrib import admin
from django.urls import path, include
from ..API.views import *

urlpatterns = [
    path('lnm/', LNMOnlineAPIView.as_view(), name="lnm-callback"),
]
