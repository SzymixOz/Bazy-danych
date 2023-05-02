from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def AddReservation(request):
    return render(request, 'add_reservation.html')

def room(request, roomId):
    return render(request, 'room.html', {'roomId': roomId})