"""
ADAPTED FROM __init__.py AT https://github.com/honeycombio/libhoney-py/
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
import secrets
import libevent.state as state
from libevent.client import Client
from libevent.constants import APP_ID_KEY, PARENT_ID_KEY, TIMESTAMP_KEY
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


def init(app_id: str = None, handlers: List[Handler] = None) -> None:
    if not app_id:
        app_id = secrets.token_hex(16).upper()
    if not handlers:
        handlers = [LogHandler.with_handler(name=app_id)]
    state.CLIENT = Client(handlers)
    state.CLIENT.add_field(APP_ID_KEY, app_id)
    state.CLIENT.add_field("initTimestamp", datetime.utcnow())
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
              calling_func: Callable = None,
              parent_id: str = None) -> Event:
    evt = Event(data=data, client=state.CLIENT)
    evt.add_field(TIMESTAMP_KEY, datetime.utcnow())
    if calling_func:
        evt.add_field('func_name', calling_func.__name__)
    if parent_id:
        evt.add_field(PARENT_ID_KEY, parent_id)
    return evt

