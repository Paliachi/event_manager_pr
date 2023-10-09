from django.contrib.auth.models import User
from django.utils import timezone

from .models import Event, EventAttendance


class RegisterUserForEventViewHelper:
    """
    Helper for implementing User registration for the event.
    """
    def __init__(self, event: Event, user: User):
        self._event_obj = event
        self._user_obj = user

    def check_capacity_of_participants(self):
        """
        Checks if all places for the event are occupied.

        :return:
        True - if there are some places left.
        None - if there is no free place.
        """
        if self._event_obj.occupied_capacity < self._event_obj.max_participants_capacity:
            self._event_obj.occupied_capacity += 1
            self._event_obj.save()

            return True
        return None

    def is_participant(self):
        """
        Checking if the user is participant of the event.

        :return:
        True - if the user is already assigned to the event.
        False - if the user is not assigned.
        """
        if EventAttendance.objects.filter(
                user_id=self._user_obj,
                event_id=self._event_obj).first():
            return True
        return False

    def register_user(self):
        event_attendance_obj = EventAttendance.objects.create(
            user_id=self._user_obj,
            event_id=self._event_obj
        )

        return event_attendance_obj

    def validate_registration_date(self):
        """
        Validates registration date of the event.
        :return:
        True - if the event's registration_end_date has not passed.
        """

        if self._event_obj.registration_end_date < timezone.now().date():
            return True
        return False
