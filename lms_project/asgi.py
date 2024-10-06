import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import lms.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            lms.routing.websocket_urlpatterns
        )
    ),
})