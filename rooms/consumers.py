from logging import exception
from urllib import request
import environ
import json, os


from asgiref.sync import async_to_sync
from channels.auth import AuthMiddlewareStack, login
from channels.generic.websocket import WebsocketConsumer
from pydantic import Json

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


class RoomConsumer(WebsocketConsumer):
    def connect(self):

        self.user = self.scope["user"]

        if self.user.is_authenticated:
            self.room_group_name = f"{self.user.username}_Music_Room"
            self.accept()

        else:
            self.close()

    def disconnect(self, close_code):
        if self.room_group_name != False:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )

    def receive(self, text_data):

        """
        Authentication via a method not through the middleware must be done using the init message.
        This is the most secure method. Also enable wss. Connection will be closed if not authenticated.
        Else connection will be established.
        """

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "playing_request", "request": text_data}
        )

    def playing_request(self, event):

        """
        This request is received by the different clients. On music play in the client a request will be sent
        via websocket connection and received here. It is then broadcasted to the each of the Users client devices.
        Handling of the request will be done on the client side.
        """

        data = json.dumps({type: "playing.request", "request": event["request"]})

        self.send(
            text_data=data,
        )
