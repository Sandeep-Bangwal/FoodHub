from django.urls import path
from .consumers import OrderTrackingConsumer, OrderNotificationConsumer


websocket_urlpatterns = [
    path('wc/OrderTrack/<id>', OrderTrackingConsumer.as_asgi()),
    path('wc/OrderNotification', OrderNotificationConsumer.as_asgi()),
]