import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from chat.models import ChatGroup, GroupMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.user = self.scope['user']
        self.group = get_object_or_404(ChatGroup, name=self.chat_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chat_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = GroupMessage.objects.create(
            group=self.group, author=self.user, body=body
        )

        async_to_sync(self.channel_layer.group_send)(
            self.chat_name,
            {
                'type': 'message_send',
                'message_id': message.id
            }
        )

    def message_send(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)

        html = render_to_string('page/chat/part/chat_message_p.html', {
            'message': message,
            'user': self.user
        })
        print(html)
        self.send(text_data=html)
