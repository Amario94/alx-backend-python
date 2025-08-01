from django.shortcuts import render, get_object_or_404
from .models import Message
from django.db.models import Prefetch


def get_thread(message):
    thread = []
    def fetch_replies(msg):
        for reply in msg.replies.all():
            thread.append(reply)
            fetch_replies(reply)
    fetch_replies(message)
    return thread


def threaded_conversation_view(request, message_id):
    root_message = get_object_or_404(Message.objects.select_related('sender', 'recipient'), id=message_id)

    # Prefetch all replies and their users
    messages = Message.objects.prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'recipient'))
    )

    thread = get_thread(root_message)
    
    return render(request, 'chat/thread.html', {
        'root_message': root_message,
        'thread': thread,
    })
