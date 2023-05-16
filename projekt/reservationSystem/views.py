from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import ReservationFilterForm, ReservationForm
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
    room_list = []
    form = ReservationFilterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            room_list = Room.objects.all()
            date = request.POST['date']
            request.session['date'] = date
            start_time = request.POST['start_time']
            request.session['start_time'] = start_time
            end_time = request.POST['end_time']
            request.session['end_time'] = end_time
            wifi = request.POST.get('wifi', None)
            projector = request.POST.get('projector', None)
            min_capacity = request.POST['min_capacity']
            max_capacity = request.POST['max_capacity']
            if min_capacity == '':
                min_capacity = 0
            if max_capacity == '':
                max_capacity = 10**10
            room_list = Room.objects.filter(capacity__gte=min_capacity, capacity__lte=max_capacity)
            if wifi != '':
                if wifi == 'True':
                    wifi = True
                else:
                    wifi = False
                room_list = room_list.filter(WiFi=wifi)
            if projector != '':
                if projector == 'True':
                    projector = True
                else:
                    projector = False
                room_list = room_list.filter(projector=projector)
            if date:
                room_list = room_list.exclude(reservation__date=date)
            if start_time:
                room_list = room_list.exclude(reservation__start_time__lte=start_time, reservation__end_time__gte=start_time)
            if end_time:
                room_list = room_list.exclude(reservation__start_time__lte=end_time, reservation__end_time__gte=end_time)
            if start_time and end_time:
                room_list = room_list.exclude(reservation__start_time__gte=start_time, reservation__end_time__lte=end_time)


        
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
    if request.method == 'POST':
        if form.is_valid():
            date = request.POST['date']
            print(date, type(date))
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            comment = request.POST['comment']
            email_adress = request.POST['email_adress']
            user = request.user
            reservation = Reservation.objects.create(date=date, start_time=start_time, end_time=end_time, comment=comment, email_adress=email_adress, room=room, user=user)
            reservation.save()
            return redirect('succesfullReservation')
    context = {
        'room': room,
        'form': form,
    }
    return render(request, 'room.html', context)

def succesfullReservation(request):
    return render(request, 'succesfullReservation.html')

def adminPanel(request):
    return render(request, 'adminPanel.html')

def handle_404(request, exception):
    return render(request, '404.html', status=404)

