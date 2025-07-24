# your_app_name/permissions.py
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    (sender or receiver) to view or manipulate messages.
    """

    def has_permission(self, request, view):
        # Require user to be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow only sender or receiver of the message
        return obj.sender == request.user or obj.receiver == request.user
