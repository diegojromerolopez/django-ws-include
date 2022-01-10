from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ws_include/$', consumers.TemplateGetter.as_asgi()),
]
