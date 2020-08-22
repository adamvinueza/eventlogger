from __future__ import annotations
from typing import Any, Dict, List, Optional
from eventlogger.event import Event
from eventlogger.handler import Handler
from eventlogger.fields import Fields
from eventlogger.log_handler import LogHandler


class Client(object):
    """Manages sending of events."""
    def __init__(self, handlers: Optional[List[Handler]] = None) -> None:
        if handlers is None:
            handlers = [LogHandler()]
        self.handlers = handlers
        self.fields = Fields()

    def add_field(self, name: str, value: Any) -> None:
        """Add a global field."""
        self.fields.add_field(name, value)

    def add(self, data: Dict) -> None:
        """Use a mappable object to add a global field."""
        self.fields.add(data)

    def send(self, evt: Event) -> None:
        """Send the event using the handlers."""
        for handler in self.handlers:
            handler.send(evt)
