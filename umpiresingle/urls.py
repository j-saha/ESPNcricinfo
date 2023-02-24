from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.umpiresingle, name='umpiresingle'),
    #path('playersingle/', include('playersingle.urls')),
]