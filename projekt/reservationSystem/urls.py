from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('room/<int:roomId>', views.room, name='room'),
    path('AddReservation/', views.AddReservation, name='AddReservation'),
    path('', views.home, name='home'),
]