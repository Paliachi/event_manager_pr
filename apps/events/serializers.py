from rest_framework import serializers

from .models import Event


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['id', 'organizator_user_id', 'occupied_capacity']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['organizator_user_id']


class EventAttendanceSerializer(serializers.Serializer):
    event_id = serializers.IntegerField(required=True, min_value=0)
