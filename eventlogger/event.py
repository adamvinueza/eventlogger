import datetime
import logging
from typing import Any, Dict, Generator, Optional
import eventlogger.state as state
from contextlib import contextmanager
from eventlogger.client import Client
from eventlogger.fields import Fields
"""
ADAPTED FROM Event CLASS AT https://github.com/honeycombio/libhoney-py
"""


class Event(object):
    """A collection of fields to be sent via a client."""
    def __init__(self,
                 data: Optional[Dict] = None,
                 fields: Fields = Fields(),
                 client: Optional[Client] = None):
        """Constructor. Should not be called """
        self.client = client
        self._fields = Fields()
        if self.client:
            self._fields += self.client.fields
        if data is None:
            data = {}
        self._fields.add(data)
        self._fields += fields

    def __getitem__(self, key: str) -> Any:
        return self._fields[key]

    def add_field(self, key: str, value: Any) -> None:
        self.add({key: value})

    def add(self, data: Dict) -> None:
        self._fields.add(data)

    def send(self) -> None:
        if self.client is None:
            state.warn_uninitialized()
            return
        self.client.send(self)

    @contextmanager
    def timer(self, name: str = 'elapsed_ms') -> Generator:
        start = datetime.datetime.now()
        yield
        duration = datetime.datetime.now() - start
        self.add_field(name, duration.total_seconds() * 1000)

    def __str__(self) -> str:
        return str(self._fields)
