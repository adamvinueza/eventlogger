import requests
from libevent import Event, Handler


class PostHandler(Handler):
    """A simple handler for sending JSON-serialized events to a remote URL."""
    def __init__(self, post_url: str):
        self.post_url = post_url

    def send(self, evt: Event) -> None:
        response = requests.post(self.post_url, json=evt.to_dict())
        response.raise_for_status()
