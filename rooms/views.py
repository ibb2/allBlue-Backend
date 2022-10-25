import json
from django.shortcuts import render

# Create your views here.


def chatroom(request):
    return render(request, 'index.html', {"room_name": "testing-room"})