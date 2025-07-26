# from django.shortcuts import render
# from rest_framework import status, filters
# from .permissions import IsParticipantOfConversation
# from rest_framework import viewsets, permissions
# from .models import Conversation, Message
# from .serializers import (
#     ConversationSerializer,
#     MessageSerializer,
#     UserSerializer,
# )
# from django.contrib.auth import get_user_model
# import django_filters
# from django_filters.rest_framework import DjangoFilterBackend
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import PageNumberPagination

# User = get_user_model()

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class ConversationViewSet(viewsets.ModelViewSet):
#     queryset = Conversation.objects.all()
#     serializer_class = ConversationSerializer
#     permission_classes = [IsParticipantOfConversation]
#     # permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         # Automatically add the request user to participants if needed
#         conversation = serializer.save()
#         conversation.participants.add(self.request.user)
#         conversation.save()

# class MessageFilter(django_filters.FilterSet):
#     sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
#     start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
#     end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

#     class Meta:
#         model = Message
#         fields = ['sender', 'start_date', 'end_date']

# class MessagePagination(PageNumberPagination):
#     page_size = 20

# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all().order_by('-sent_at')
#     serializer_class = MessageSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = MessageFilter
#     pagination_class = MessagePagination

#     def get_queryset(self):
#         conversation_id = self.kwargs.get('conversation_pk')
#         return Message.objects.filter(conversation_id=conversation_id).order_by('-sent_at')

#     def perform_create(self, serializer):
#         conversation_id = self.kwargs.get('conversation_pk')
#         serializer.save(
#             conversation_id=conversation_id,
#             sender=self.request.user
#         )

from django.shortcuts import render 
from rest_framework import status, filters
from rest_framework.response import Response  # ✅ Import this
from .permissions import IsParticipantOfConversation
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    UserSerializer,
)
from django.contrib.auth import get_user_model
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .pagination import MessagePagination

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsParticipantOfConversation]

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

    def retrieve(self, request, *args, **kwargs):
        conversation = self.get_object()
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().retrieve(request, *args, **kwargs)

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    # def get_queryset(self):
    #     conversation_id = self.kwargs.get('conversation_pk')
    #     return Message.objects.filter(
    #         conversation_id=conversation_id,
    #         conversation__participants=self.request.user
    #     ).order_by('-sent_at')
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Message.objects.none()  # No results for unauthenticated users

        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        ).order_by('-sent_at')


    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(id=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not authorized to send messages in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(
            conversation_id=conversation_id,
            sender=self.request.user
        )
