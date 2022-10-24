from django.urls import re_path

websocket_repaths = [
    re_path(r'^ws/$', websocket_handler, name='websocket_handler'),
]