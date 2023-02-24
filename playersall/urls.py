from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.playersall, name='playersall'),
    path('playersingle/', include('playersingle.urls')),
]