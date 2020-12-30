from __future__ import annotations
from typing import Any, Dict, List, Optional
from libevent.handler import Handler
from libevent.stdout_handler import StdoutHandler
from libevent.fields import Fields
from libevent.event import Event


class Client(Handler):

    """Manages the sending of events."""
    def __init__(self, handlers: Optional[List[Handler]] = None) -> None:
        if handlers is None:
            handlers = [StdoutHandler()]
        self.handlers = handlers
        self.fields = Fields()

    def __getitem__(self, key):
        return self.fields[key]

    def __contains__(self, key):
        return key in self.fields

    def add(self, data: Dict) -> None:
        """Use a mappable object to add a global field."""
        self.fields.add(data)

    def add_field(self, name: str, value: Any) -> None:
        """Add a global field."""
        self.fields.add_field(name, value)

    def new_event(self, data: Optional[Dict] = None):
        return Event(data=data, client=self)

    def send(self, evt: Any) -> None:
        """Send the event using the handlers."""
        for handler in self.handlers:
            handler.send(evt)
