from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from chatapp.models import ChatMessage,ChatRoom
from django.contrib.auth.models import User
from django.http import HttpResponse
class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("hey connect called ")
        await self.accept()

    async def disconnect(self):
        print("hey disconnect called ")
        await self.channel_layer.group_discard(
            self.channel_name,
            self.room_group_name
        )
    #receiving message from client and adding to channel layer
    async def receive(self,text_data):
        print("hey receive called ")
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        

        if not username:
            return 
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message':message,
                'username':username,
                'room':room,
            }
        )
        await self.save_message(username=username,room=room,message=message)
    #sending back to client 
    async def chat_message(self,event):
        print("hey chat_message called ")
        message = event['message']
        username = event['username']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'room':room,
        }))

    @sync_to_async
    def save_message(self,username,room,message):
        try:
            user = User.objects.get(username=username)
            room = ChatRoom.objects.get(slug=room)
            ChatMessage.objects.create(user=user,room=room,message_content=message)
        except:
            print("please login")
            return HttpResponse("please login")