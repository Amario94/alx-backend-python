from rest_framework import serializers
from .models import Message, Conversation
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(max_length=1000)
    sent_time = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_sent_time(self, obj):
        return obj.sent_at.strftime("%Y-%m-%d %H:%M:%S")


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']

    def validate(self, data):
        if 'participants' in self.initial_data:
            if len(self.initial_data['participants']) < 2:
                raise serializers.ValidationError("A conversation must have at least two participants.")
        return data
