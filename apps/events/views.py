from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from rest_framework import status, permissions, filters
from rest_framework.response import Response
import django_filters

from .models import Event, EventAttendance
from .serializers import (
    CreateEventSerializer,
    EventSerializer,
    EventAttendanceSerializer
)
from .filters import EventFilter
from .permissions import IsEventOrganizator
from .utilities import RegisterUserForEventViewHelper


class CreateEventView(CreateAPIView):
    """
    POST: Creates Event.
    """
    serializer_class = CreateEventSerializer
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(organizator_user_id=user)


class ListUserEventsView(ListAPIView):
    """
    GET: Retrieves all events of the particular user.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Event.objects.filter(organizator_user_id=user)
        return queryset


class ListEventsView(ListAPIView):
    """
    GET: Retrieves all events.
    Usage: Adding parameter ?registration_end_date to endpoint filters the last day of registration.
    For example, if registration end date is 2023-10-9,
    then appears all events with deadline of 2023-10-9 and earlier.
    The same principe for ?participants_quantity.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EventFilter
    permission_classes = [permissions.IsAuthenticated]


class UpdateEventView(UpdateAPIView):
    """
    PATCH: Updates particular event.
    NOTE: Only Owner of the event can update the object.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizator]
    allowed_methods = ['PATCH']

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Event.objects.none()

        queryset = Event.objects.filter(organizator_user_id=self.request.user)
        return queryset


class DeleteEventView(DestroyAPIView):
    """
    DELETE: Destroys the event created by the particular user.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizator]
    queryset = Event.objects.all()


class RegisterUserForEventView(CreateAPIView):
    """
    Register user to the event.
    Note: The owner of the event can not be registered.
    """
    serializer_class = EventAttendanceSerializer
    queryset = EventAttendance.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizator]

    def create(self, request, *args, **kwargs):
        serialized_data = self.get_serializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        event_id = serialized_data.validated_data.get("event_id")
        user = self.request.user

        try:
            event = Event.objects.get(pk=event_id)

        except Event.DoesNotExist:
            return Response(
                {'error': 'The Event does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        event_attendance_helper = RegisterUserForEventViewHelper(event, user)
        if event_attendance_helper.is_participant():
            return Response(
                {"error": "User is registered already."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not event_attendance_helper.validate_registration_date():
            return Response(
                {"error": "Registration date for the event has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not event_attendance_helper.check_capacity_of_participants():
            return Response(
                {"error": "There is no free space left for the event. "
                          "The User can not be registered"},
                status=status.HTTP_400_BAD_REQUEST
            )

        event_attendance_helper.register_user()

        return Response(
            {'message': 'User registered for event successfully.'},
            status=status.HTTP_201_CREATED
        )


class UnregisterFromEventView(DestroyAPIView):
    """
    DELETE: Unregisters user from the event.
    """
    serializer_class = EventAttendanceSerializer
    queryset = EventAttendance.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        event_attendance_helper = RegisterUserForEventViewHelper(
            instance,
            self.request.user
        )
        if not event_attendance_helper.validate_registration_date():
            return Response(
                {"error": "Registration date for the event has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(
            {"message": "The User was unregistered successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


