from __future__ import annotations
from typing import Any, Dict, List, Optional
from libevent.handler import Handler
from libevent.log_handler import LogHandler
from libevent.fields import Fields


class Client(Handler):
    """Manages sending of events."""
    def __init__(self, handlers: Optional[List[Handler]] = None) -> None:
        if handlers is None:
            handlers = [LogHandler()]
        self.handlers = handlers
        self.fields = Fields()

    def __getitem__(self, key):
        return self.fields[key]

    def __contains__(self, key):
        return key in self.fields

    def add_field(self, name: str, value: Any) -> None:
        """Add a global field."""
        self.fields.add_field(name, value)

    def add(self, data: Dict) -> None:
        """Use a mappable object to add a global field."""
        self.fields.add(data)

    def send(self, evt: Any) -> None:
        """Send the event using the handlers."""
        for handler in self.handlers:
            handler.send(evt)
