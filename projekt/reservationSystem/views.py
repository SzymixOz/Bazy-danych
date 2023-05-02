from django.shortcuts import render

from .models import Room

# Create your views here.

def home(request):
    room_list = Room.objects.all()
    print(room_list)
    return render(request, 'home.html',
                  {'room_list': room_list})

def AddReservation(request):
    return render(request, 'add_reservation.html')

def room(request, roomId):
    return render(request, 'room.html', {'roomId': roomId})