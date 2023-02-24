from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.umpiresall, name='umpiresall'),
    path('umpiresingle/', include('umpiresingle.urls')),
]