from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from reservationSystem.models import Room, Reservation
from django.contrib.auth.models import User

from .models import Room

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rejestracja zakończona sukcesem. Możesz się teraz zalogować.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nieprawidłowe dane logowania.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



def home(request):
    min_capacity = request.GET.get('min_capacity')
    max_capacity = request.GET.get('max_capacity')
    wifi = request.GET.get('wifi')
    projector = request.GET.get('projector')
    date = request.GET.get('date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    room_list = Room.objects.all()

    if min_capacity:
        room_list = room_list.filter(capacity__gte=min_capacity)
    if max_capacity:
        room_list = room_list.filter(capacity__lte=max_capacity)
    if wifi:
        room_list = room_list.filter(WiFi=(wifi == 'tak'))
    if projector:
        room_list = room_list.filter(projector=(projector == 'tak'))
    if date and start_time and end_time:
        reservations = Reservation.objects.filter(
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).values_list('room_id', flat=True)
        room_list = room_list.exclude(id__in=reservations)
    return render(request, 'home.html',
                  {'room_list': room_list})

def AddReservation(request):
    return render(request, 'add_reservation.html')

def room(request, roomId):
    try:
        room = Room.objects.get(id=roomId)
    except Room.DoesNotExist:
        return home(request)
    return render(request, 'room.html', {'room': room})

def adminPanel(request):
    return render(request, 'adminPanel.html')

def handler404(request, exception):
    return render(request, '404.html')

