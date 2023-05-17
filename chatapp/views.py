from django.shortcuts import render
from chatapp.models import ChatRoom,ChatMessage
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request,"chatapp/index.html",context={
        'chatrooms':chat_rooms
    })

def room(request,room_name):
    messages = ChatMessage.objects.filter(room__slug=room_name)[:30]
    context = {
        "chatroom":ChatRoom.objects.get(slug=room_name),
        "messages":messages
        }
    return render(request,"chatapp/chat-room.html",context)