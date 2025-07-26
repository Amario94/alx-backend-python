# from rest_framework import permissions

# class IsParticipantOfConversation(permissions.BasePermission):
#     """
#     Custom permission to only allow participants of a conversation
#     (sender or receiver) to view or send messages.
#     Only the sender can update or delete the message.
#     """

#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         # Allow GET or POST if user is sender or receiver
#         if request.method in permissions.SAFE_METHODS or request.method == "POST":
#             return obj.sender == request.user or obj.receiver == request.user

#         # Only the sender can update or delete the message
#         if request.method in ["PUT", "PATCH", "DELETE"]:
#             return obj.sender == request.user

#         return False

# chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        conversation_id = view.kwargs.get('conversation_pk')
        if not request.user or not request.user.is_authenticated:
            return False
        return True  # permission is granted for authenticated users

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user in obj.participants.all()
