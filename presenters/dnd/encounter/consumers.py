# chat/consumers.py
import json
from pprint import pprint

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from encounter.models import Character


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'chat_'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        # Receive message from WebSocket

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        members = text_data_json['members']
        players = text_data_json['players']
        for player in players:
            character=Character.objects.get(id=player['id'])
            character.hitpoints=player['hp']
            character.save()
        author = text_data_json['author']
        _map = text_data_json['map']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'members': members,
                'players': players,
                'author': author,
                'map': _map,
                'encounterID': text_data_json['encounterID']
            }
        )

        # Receive message from room group

    def chat_message(self, event):
        pprint(event)
        members = event['members']
        players = event['players']
        author = event.get('author', 'nobody')
        _map = event.get('map', 'no_map')

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'members': members,
            'players': players,
            'author': author,
            'map': _map,
            'encounterID': event.get('encounterID', 100)
        }))
