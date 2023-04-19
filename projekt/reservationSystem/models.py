from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Reservation(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    def __str__(self):
        return f'{self.room} {self.date} {self.start_time}'