from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.playerofateam, name='playerofateam'),
    path('playersingle/', include('playersingle.urls')),
]