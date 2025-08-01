from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render

from messaging.models import Message


@cache_page(60)  # Cache for 60 seconds
def message_list(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id)
    return render(request, 'chats/message_list.html', {'messages': messages})
