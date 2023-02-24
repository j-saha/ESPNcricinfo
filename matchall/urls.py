from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.matchall, name='matchall'),
    path('matchsingle/', include('matchsingle.urls')),
]