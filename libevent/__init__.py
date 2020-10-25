"""
ADAPTED FROM __init__.py AT https://github.com/honeycombio/libhoney-py/
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
import secrets

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

EVENT_ID_KEY = "eventId"
PARENT_ID_KEY = "parentId"
TIMESTAMP_KEY = "timestamp"


def init(app_id: str = None, handlers: Optional[List[Handler]] = None) -> None:
    if handlers is None:
        handlers = [LogHandler()]
    state.CLIENT = Client(handlers)
    if app_id:
        state.CLIENT.add_field("applicationId", app_id)
    state.CLIENT.add_field("initTimestamp", datetime.now().isoformat())
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
    evt.add_field(TIMESTAMP_KEY, datetime.now())
    evt.add_field(EVENT_ID_KEY, secrets.token_hex(8))
    if calling_func:
        evt.add_field('func_name', calling_func.__name__)
    return evt


def event_chain(data: Optional[Dict] = None,
                calling_func: Callable = None,
                parent: Event = None):
    evt = new_event(data, calling_func)
    if parent:
        if EVENT_ID_KEY in parent:
            evt.add_field(PARENT_ID_KEY, parent[EVENT_ID_KEY])
    return evt
