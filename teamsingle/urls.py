from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.teamsingle, name='teamsingle'),
    path('playerofateam/', include('playerofateam.urls')),

]