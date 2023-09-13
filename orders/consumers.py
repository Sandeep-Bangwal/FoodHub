from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import *
from django.core.serializers.json import DjangoJSONEncoder

class OrderTrackingConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'order_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)( self.room_group_name, self.channel_name)
        order = Orders.give_order_details(self.room_name)
        self.accept()
        self.send(text_data=json.dumps({
           'payload': order
        }))


    # Receive message from WebSocket
    def receive(self, text_data):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status',
                'payload': text_data
            }
        )

    # Receive message from room group
    def order_status(self, event):
        print(event)
        data = json.loads(event['value'])
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'payload': data
        }))  

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
      )  
        
class OrderNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'notification'
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
      
        self.accept() 
       

    def receive(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            'type': 'Order.Notification',
             'payload': text_data,
        })
        print(text_data)  
        
    def Order_Notification(self, event):
        data = json.loads(event['value'])
        print("data is the.......", data)
        print(type(data))
        self.send(text_data=json.dumps(
        {
            'payload': data
        }
        ))  

    async def close(self, code=None):
        print("close")        