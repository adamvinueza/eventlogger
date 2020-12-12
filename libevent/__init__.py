"""
ADAPTED FROM __init__.py AT https://github.com/honeycombio/libhoney-py/
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
import secrets
import libevent.constants as constants
import libevent.state as state
from libevent.client import Client
from libevent.event import Event
from libevent.fields import Fields
from libevent.handler import Handler
from libevent.log_handler import LogHandler
from libevent.trace import Tracer


"""
Sample usage:

    libevent.init()
    # ...
    evt = libevent.new_event()
    evt.add_field(...)
    # ...
    evt.send()
"""

_GLOBAL_TRACER = None


def init(app_id: str = None, handlers: List[Handler] = None) -> None:
    if not app_id:
        app_id = secrets.token_hex(16).upper()
    if not handlers:
        handlers = [LogHandler.with_handler(name=app_id)]
    state.CLIENT = Client(handlers)
    state.CLIENT.add_field(constants.APP_ID_KEY, app_id)
    state.CLIENT.add_field(constants.INIT_TIMESTAMP_KEY, datetime.utcnow())
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
              parent_id: str = None,
              event_id: str = None) -> Event:
    evt = Event(data=data, client=state.CLIENT, event_id=event_id)
    evt.add_field(constants.TIMESTAMP_KEY, datetime.utcnow())
    if calling_func:
        evt.add_field(constants.OPERATION_KEY, calling_func.__name__)
    if parent_id:
        evt.add_field(constants.PARENT_ID_KEY, parent_id)
    return evt


def new_trace_id():
    return secrets.token_hex(8)


def get_tracer(auto: bool = True):
    global _GLOBAL_TRACER
    if not _GLOBAL_TRACER:
        _GLOBAL_TRACER = Tracer(auto=auto)
    return _GLOBAL_TRACER

