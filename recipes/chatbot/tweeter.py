import os

from tweepy import Client

api_key = os.environ["X_API_KEY"]
api_key_secret = os.environ["X_API_KEY_SECRET"]
bearer_token = os.environ["X_BEARER_TOKEN"]
access_token = os.environ["X_ACCESS_TOKEN"]
access_token_secret = os.environ["X_ACCESS_TOKEN_SECRET"]


def post(content: str) -> None:
    client = Client(
        bearer_token,
        api_key,
        api_key_secret,
        access_token,
        access_token_secret
    )

    client.create_tweet(text=content)
