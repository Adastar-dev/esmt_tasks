import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.projet_id = self.scope['url_route']['kwargs']['projet_id']
        self.room_group_name = f'chat_{self.projet_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        contenu = data['message']
        username = data['username']

        await self.save_message(username, self.projet_id, contenu)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': contenu,
                'username': username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def save_message(self, username, projet_id, contenu):
        from accounts.models import User
        from projects.models import Project
        from .models import Message
        user = User.objects.get(username=username)
        projet = Project.objects.get(pk=projet_id)
        Message.objects.create(auteur=user, projet=projet, contenu=contenu)