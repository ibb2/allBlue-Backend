import environ
import firebase_admin
import json 

from channels.generic.websocket import WebsocketConsumer
from firebase_admin import credentials
from pydantic import Json

class RoomConsumer(WebsocketConsumer):

    def connect(self, identifier):
        # On connect verification will be performed, Via firebase-admin
        cred = credentials.Certificate(environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        verified =firebase_admin.initialize_app(cred)

        id_token = Json.loads(identifier)
        decoded_token = firebase_admin.verify_id_token(id_token)
        uid = decoded_token["uid"]

        if (uid != None):
            self.accept()


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))

