from django.urls import path

from .views import (
    CreateEventView,
    ListUserEventsView,
    ListEventsView,
    UpdateEventView,
    DeleteEventView,
    RegisterUserForEventView,
    UnregisterFromEventView
)


urlpatterns = [
    path("create_event/", CreateEventView.as_view(), name="create_event"),
    path("list/user_events/", ListUserEventsView.as_view(), name="user_events_list"),
    path("list_events/", ListEventsView.as_view(), name="events_list"),
    path("update_event/<int:pk>/", UpdateEventView.as_view(), name="update_event"),
    path("delete_event/<int:pk>/", DeleteEventView.as_view(), name="delete_event"),
    path("register_for_event/",
         RegisterUserForEventView.as_view(),
         name="register_for_event"),
    path("unregister_from_event/<int:pk>",
         UnregisterFromEventView.as_view(),
         name="unregister_from_event"),
]
