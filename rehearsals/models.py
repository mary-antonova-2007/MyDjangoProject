from django.db import models


class RehearsalDate(models.Model):
    date = models.DateField()
    description = models.TextField()


class Room(models.Model):
    room_number = models.IntegerField()
    floor = models.IntegerField()
    rehearsal_date = models.ForeignKey(RehearsalDate, on_delete=models.CASCADE)


class Window(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_light_on = models.BooleanField()
