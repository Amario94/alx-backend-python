# your_app_name/permissions.py
# from rest_framework import permissions

# class IsParticipantOfConversation(permissions.BasePermission):
#     """
#     Custom permission to only allow participants of a conversation
#     (sender or receiver) to view or manipulate messages.
#     """

#     def has_permission(self, request, view):
#         # Require user to be authenticated
#         return request.user and request.user.is_authenticated
    
#     def has_object_permission(self, request, view, obj):
#         # Everyone (sender or receiver) can view
#         if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
#             return obj.sender == request.user or obj.receiver == request.user

#         # Only sender can edit or delete
#         return obj.sender == request.user


from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    (sender or receiver) to view or send messages.
    Only the sender can update or delete the message.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow GET or POST if user is sender or receiver
        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return obj.sender == request.user or obj.receiver == request.user

        # Only the sender can update or delete the message
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.sender == request.user

        return False
