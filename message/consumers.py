from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Messages
from django.shortcuts import get_object_or_404
from users.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def get_previous_messages(self, data=None):
        messages = Messages.last_30_messages()
        content = {
            'messages': messages
        }
        await self.send_chat_message(content)

    async def new_message(self, data):
        author = data['from']
        author_user = get_object_or_404(User, username=author)
        pass

    async def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'dateSent': str(message.dateSent)
        }

    async def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(result.append(self.message_to_json(message)))
        return result

    commands = {
        'get_previous_messages': get_previous_messages,
        'new_message': new_message
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        print('received')
        data = json.loads(text_data)
        await self.commands[data['command']](data)

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'message_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.scope['user'])
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
