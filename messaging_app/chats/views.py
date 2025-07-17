from django.shortcuts import render
from rest_framework import status, filters

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    UserSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically add the request user to participants if needed
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        serializer.save(
            conversation_id=conversation_id,
            sender=self.request.user
        )
