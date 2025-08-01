from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from messaging.models import Notification
from django.shortcuts import render, get_object_or_404
from .models import Message
from django.contrib.auth.decorators import login_required

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