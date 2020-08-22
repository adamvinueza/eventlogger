"""
ADAPTED FROM __init__.py AT https://github.com/honeycombio/libhoney-py/
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
import eventlogger.state as state
from eventlogger.client import Client
from eventlogger.handler import Handler
from eventlogger.log_handler import LogHandler
from eventlogger.event import Event

"""
Sample usage:

    eventlogger.init()
    # ...
    evt = eventlogger.new_event()
    evt.add_field(...)
    # ...
    evt.send()
"""


def init(handlers: Optional[List[Handler]] = None) -> None:
    if handlers is None:
        handlers = [LogHandler()]
    state.CLIENT = Client(handlers)


def add_field(name: str, val: Any) -> None:
    if state.CLIENT is None:
        state.warn_uninitialized()
        return
    state.CLIENT.add_field(name, val)


def add(data: Dict) -> None:
    if state.CLIENT is None:
        state.warn_uninitialized()
        return
    state.CLIENT.add(data)


def new_event(data: Optional[Dict] = None) -> Event:
    return Event(data)
