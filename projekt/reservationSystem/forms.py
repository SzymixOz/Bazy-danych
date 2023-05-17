from django import forms
from django.forms import ModelForm, Form
from .models import Reservation, Room

class ReservationFilterForm(Form):
    CHOICES = [
        (None, '---------'),
        (True, 'Tak'),
        (False, 'Nie'),
    ]
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    wifi = forms.CharField(widget=forms.Select(choices=CHOICES), required=False)
    projector = forms.CharField(widget=forms.Select(choices=CHOICES), required=False)
    min_capacity = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'number'}), required=False)
    max_capacity = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'number'}), required=False)

class ReservationForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 50}), required=False)
    class Meta:
        model = Reservation
        fields = ['date', 'start_time', 'end_time', 'comment', 'email_adress']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
            'email_adress': forms.EmailInput(attrs={'type': 'email'}),
        }

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'WiFi', 'projector', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'type': 'text'},),
            'capacity': forms.NumberInput(attrs={'type': 'number'}),
            'WiFi': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            'projector': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
        }

        # def clean(self):
        #     cleaned_data = super().clean()
        #     name = cleaned_data.get('name')
        #     capacity = cleaned_data.get('capacity')
        #     WiFi = cleaned_data.get('WiFi')
        #     projector = cleaned_data.get('projector')

        #     if not name or not capacity or WiFi is None or projector is None:
        #         raise forms.ValidationError("Wszystkie pola są wymagane.")

        #     return cleaned_data
        




