# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from applications.chat.models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json["content"]
        profile_pk = text_data_json["profile_pk"]
        chat_id = int(text_data_json["room_name"])

        message = Message.objects.create(
            content=content, author_id=profile_pk, chat_id=chat_id
        )
        message.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "content": message.content,
                "message_pk": message.pk,
                "profile_pk": profile_pk,
                "datetime": message.get_datetime,
            },
        )

    # Receive message from room group
    def chat_message(self, event):
        content = event["content"]
        author_pk = event["profile_pk"]
        datetime = event["datetime"]
        pk = event["message_pk"]

        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "content": content,
                    "message_pk": pk,
                    "profile_pk": author_pk,
                    "datetime": datetime,
                }
            )
        )
