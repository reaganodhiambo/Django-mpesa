from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('c2b/', views.c2b),
    path('lipa/', views.lipaNaMpesa),
    path('mpesa/', include('mpesa.urls')),
    path('new/',views.new),
    path('confirm/', views.confirmation),
    path('validate/', views.validation),

]
