from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from messaging.models import Notification
from .models import Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


from messaging.models import Message

def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification.html', {'notifications': notifications})



def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'message_detail.html', {'message': message})




@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect('home')  # or login page
    

def inbox_view(request):
    user = request.user
    unread_messages = Message.unread.for_user(user)
    return render(request, 'inbox.html', {'unread_messages': unread_messages})

@login_required
def sent_messages_view(request):
    """
    View that shows messages sent by the current user to a specific receiver.
    """
    receiver_id = request.GET.get("receiver_id")
    if not receiver_id:
        return render(request, "messaging/sent_messages.html", {"messages": [], "error": "No receiver specified"})

    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return render(request, "messaging/sent_messages.html", {"messages": [], "error": "Receiver not found"})

    # Use select_related to optimize the query
    messages = Message.objects.filter(sender=request.user, receiver=receiver).select_related('sender', 'receiver')

    return render(request, "messaging/sent_messages.html", {"messages": messages})




@cache_page(60)  # Cache for 60 seconds
def message_list(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id)
    return render(request, 'chats/message_list.html', {'messages': messages})

from django.contrib.auth.decorators import login_required
from .models import Message

# @login_required
# def unread_messages_view(request):
#     unread_messages = Message.unread.unread_for_user(request.user).only('id', 'content', 'sender', 'created_at').select_related('sender')

#     return render(request, 'messaging/unread_messages.html', {
#         'unread_messages': unread_messages
#     })