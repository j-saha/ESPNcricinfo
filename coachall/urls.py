from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.coachall, name='coachall'),
    path('coachsingle/', include('coachsingle.urls')),
]