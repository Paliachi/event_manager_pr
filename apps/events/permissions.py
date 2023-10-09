from rest_framework.permissions import BasePermission


class IsEventOrganizator(BasePermission):
    def has_object_permission(self, request, view, event_obj):
        return event_obj.organizator_user_id == request.user
