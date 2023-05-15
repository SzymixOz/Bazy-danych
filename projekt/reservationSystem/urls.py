from django.urls import path
from . import views

handler404 = 'django.views.defaults.page_not_found'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('room/<int:roomId>', views.room, name='room'),
    path('AddReservation/', views.AddReservation, name='AddReservation'),
    path('', views.home, name='home'),
]