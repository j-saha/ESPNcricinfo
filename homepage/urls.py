from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams, name='teams'),
    path('series_details/', views.series_details, name='series_details'),
    path('login/', include('loginpage.urls')),
    path('seriesall/', include('seriesall.urls')),
    path('playersall/', include('playersall.urls')),
    path('grounds/', include('grounds.urls')),
    path('playersingle/', include('playersingle.urls')),
    path('umpiresall/', include('umpiresall.urls')),
    path('coachall/', include('coachall.urls')),
    path('matchall/', include('matchall.urls')),
    path('teamsingle/', include('teamsingle.urls')),
    path('records/', include('records.urls')),
]
