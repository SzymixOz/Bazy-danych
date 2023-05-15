from django.urls import path
from django.contrib import admin
from . import views
from django.conf.urls import handler404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

handler404 = 'django.views.defaults.page_not_found'

def staff_check(user):
    return user.is_staff

def admin_panel_view(request):
    if not request.user.is_staff:
        return redirect('/reservationSystem/')
    return render(request, 'adminPanel.html')

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('room/<int:roomId>', views.room, name='room'),
    path('AddReservation/', views.AddReservation, name='AddReservation'),
    path('adminPanel/', admin_panel_view, name='adminPanel'),
    path('', views.home, name='home'),
]