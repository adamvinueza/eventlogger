"""
ADAPTED FROM __init__.py AT https://github.com/honeycombio/libhoney-py/
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import libevent.state as state
from libevent.client import Client
from libevent.event import Event
from libevent.handler import Handler
from libevent.log_handler import LogHandler

"""
Sample usage:

    libevent.init()
    # ...
    evt = libevent.new_event()
    evt.add_field(...)
    # ...
    evt.send()
"""


def init(handlers: Optional[List[Handler]] = None) -> None:
    if handlers is None:
        handlers = [LogHandler()]
    state.CLIENT = Client(handlers)
    # Set to False to not spam handlers with warnings if we call init late.
    state.WARNED_UNINITIALIZED = False


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


def new_event(data: Optional[Dict] = None,
              calling_func: Callable = None) -> Event:
    evt = Event(data=data, client=state.CLIENT)
    evt.add_field('timestamp', datetime.now())
    if calling_func:
        evt.add_field('func_name', calling_func.__name__)
    return evt
