from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('messenger/updates/', consumers.MessenerConsumer.as_asgi()),
]
