from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    registration_end_date = models.DateField()
    max_participants_capacity = models.IntegerField()
    occupied_capacity = models.IntegerField(default=0)
    organizator_user_id = models.ForeignKey(
        User,
        related_query_name="events",
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        self.title


class EventAttendance(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'event_id')

