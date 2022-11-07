"""General web socket middlewares
"""

import environ, firebase_admin, os
from pathlib import Path

from firebase_admin import auth, credentials
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent


@database_sync_to_async
def get_user(validated_data):
    try:
        user, created = get_user_model().objects.get_or_create(
            username=validated_data["uid"], email=validated_data["email"]
        )

        # return get_user_model().objects.get(id=token_id)
        print(f"{user}, {created}")
        print("User successfully created")
        return user

    except Exception as e:
        print(e)
        return AnonymousUser()


class FirebaseAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token
        id_token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        print(id_token)

        # Try to authenticate the user
        try:
            pathToCredentials = "{}".format(
                os.path.join(BASE_DIR, env("FIREBASE_ADMIN_SDK_CREDENTIALS"))
            )

            cred = credentials.Certificate(pathToCredentials)
            firebase_admin.initialize_app(cred)

        except Exception as e:
            # Token is invalid
            print(e)
            return None
        else:
            #  Then token is valid, decode it
            decoded_data = auth.verify_id_token(id_token)
            uid = decoded_data["uid"]

            # Get/Create the user using ID
            scope["user"] = await get_user(decoded_data)
        return await super().__call__(scope, receive, send)


def FirebaseAuthMiddlewareStack(inner):
    return FirebaseAuthMiddleware(AuthMiddlewareStack(inner))
