import datetime
from time import sleep
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import ReservationFilterForm, ReservationForm, RoomForm
from reservationSystem.models import Room, Reservation
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Equipment, Room

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
    room_list = []
    form = ReservationFilterForm(request.POST)
    if request.method == 'POST':
        query = Q()
        if form.is_valid():
            date = request.POST['date']
            if date < str(datetime.date.today()) and date != '':
                messages.error(request, 'Nie można zarezerwować pokoju w przeszłości.')
                return render(request, 'home.html', {'form': form})
            request.session['date'] = date
            start_time = request.POST['start_time']
            request.session['start_time'] = start_time
            end_time = request.POST['end_time']
            if start_time >= end_time and start_time != '' and end_time != '':
                messages.error(request, 'Godzina rozpoczęcia musi być wcześniejsza od godziny zakończenia.')
                return render(request, 'home.html', {'form': form})
            request.session['end_time'] = end_time
            wifi = request.POST.get('wifi', None)
            projector = request.POST.get('projector', None)
            min_capacity = request.POST['min_capacity']
            max_capacity = request.POST['max_capacity']
            if min_capacity != '' and min_capacity != '' and (int(min_capacity) < 0 or int(max_capacity) < 0):
                messages.error(request, 'Pojemność sali nie może być ujemna.')
                return render(request, 'home.html', {'form': form})
            if min_capacity == '':
                min_capacity = 0
            if max_capacity == '':
                max_capacity = 10**10
            
            if min_capacity:
                query &= Q(capacity__gte=min_capacity)
            if max_capacity:
                query &= Q(capacity__lte=max_capacity)
            if wifi:
                if wifi == 'True':
                    query &= Q(WiFi=True)
                else:
                    query &= Q(WiFi=False)
            if projector:
                if projector == 'True':
                    query &= Q(projector=True)
                else:
                    query &= Q(projector=False)
            if date:
                query &= ~Q(reservation__date=date)
            if start_time:
                query &= ~Q(reservation__start_time__lte=start_time, reservation__end_time__gte=start_time, reservation__date=date)
            if end_time:
                query &= ~Q(reservation__start_time__lte=end_time, reservation__end_time__gte=end_time, reservation__date=date)
            if start_time and end_time:
                query &= ~Q(reservation__start_time__gte=start_time, reservation__end_time__lte=end_time, reservation__date=date)
            room_list = Room.objects.filter(query)

    context = {
        'room_list': room_list,
        'form': form,
    }
    return render(request, 'home.html', context)

def AddReservation(request):
    return render(request, 'add_reservation.html')

def room(request, roomId):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        room = Room.objects.get(id=roomId)
    except Room.DoesNotExist:
        return home(request)
    date = request.session.get('date', None)
    start_time = request.session.get('start_time', None)
    end_time = request.session.get('end_time', None)
    form = ReservationForm(request.POST or None, initial={'date': date, 'start_time': start_time, 'end_time': end_time})
    context = {
        'room': room,
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            date = request.POST['date']
            if date < str(datetime.date.today()):
                messages.error(request, 'Nie można zarezerwować pokoju w przeszłości.')
                return render(request, 'room.html', context)
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            if start_time >= end_time:
                messages.error(request, 'Godzina rozpoczęcia musi być wcześniejsza od godziny zakończenia.')
                return render(request, 'room.html', context)
            comment = request.POST['comment']
            email_adress = request.POST['email_adress']
            user = request.user
            if not checkroom(room, date, start_time, end_time):
                messages.error(request, 'Pokój jest już zarezerwowany w tym terminie.')
            else:
                reservation = Reservation.objects.create(date=date, start_time=start_time, end_time=end_time, comment=comment, email_adress=email_adress, room=room, user=user)
                reservation.save()
                return redirect('succesfullReservation')
    return render(request, 'room.html', context)

def checkroom(room, date, start_time, end_time):
    reservations = Reservation.objects.filter(room=room, date=date)
    reservations = reservations.filter(
    Q(start_time__lte=start_time, end_time__gte=start_time) |
    Q(start_time__lte=end_time, end_time__gte=end_time) |
    Q(start_time__gte=start_time, end_time__lte=end_time) |
    Q(start_time__lte=start_time, end_time__gte=end_time)
    )   
    if reservations:
        return False
    return True


def succesfullReservation(request):
    return render(request, 'succesfullReservation.html')

def adminPanel(request):
    return render(request, 'adminPanel.html')

def rooms(request):
    rooms = Equipment.objects.all()
    context = {
        'room_list': rooms,
    }
    return render(request, 'rooms.html', context)

def addRoom(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = request.POST['name']
            capacity = request.POST['capacity']
            WiFi = request.POST.get('WiFi', None)
            projector = request.POST.get('projector', None)
            computers = request.POST.get('computers', None)
            description = request.POST['description']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            room = Room.objects.create(name=name, description=description)
            equipment = Equipment.objects.create(room=room, capacity=capacity, WiFi=WiFi, projector=projector,
                                                computers=computers, start_date=start_date, end_date=end_date)
            room.save()
            equipment.save()
            return redirect('rooms')
    context = {
        'form': form,
    }
    return render(request, 'addRoom.html', context)

def roomAdmin(request, roomId):
    try:
        room = Room.objects.get(id=roomId)
    except Room.DoesNotExist:
        return redirect('rooms')
    
    form = RoomForm(request.POST or None, initial={'name': room.name, 'capacity': room.capacity, 'WiFi': room.WiFi, 'projector': room.projector, 'description': room.description})
    if request.method == 'POST':
        if form.is_valid():
            name = request.POST['name']
            capacity = request.POST['capacity']
            WiFi = request.POST.get('WiFi', None)
            projector = request.POST.get('projector', None)
            description = request.POST['description']
            new_room = Room.objects.create(name=name, capacity=capacity, WiFi=WiFi, projector=projector, description=description, expiry_date=None)
            new_room.save()
            room.expiry_date = datetime.date.today() + datetime.timedelta(days=60)
            room.save()
            return redirect('rooms')
    context = {
        'form': form,
    }
    return render(request, 'roomAdmin.html', context)

def delete_room(request, roomId):
    try:
        room = Room.objects.get(id=roomId)
    except Room.DoesNotExist:
        return redirect('rooms')
    
    room.delete()
    return redirect('rooms')

def handle_404(request, exception):
    return render(request, '404.html', status=404)

