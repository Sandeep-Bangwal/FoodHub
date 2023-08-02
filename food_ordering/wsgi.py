import os
from django.core.wsgi import get_wsgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_ordering.settings')

application = ProtocolTypeRouter({
    'http':get_wsgi_application(),
})
