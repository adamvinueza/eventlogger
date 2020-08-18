"""
ADAPTED FROM __init__.py AT https://github.com/honeycombio/libhoney-py/
"""
import logging
import eventlogger.state as state
from eventlogger.logclient import LogClient
from eventlogger.event import Event


def init(logger=None):
    if logger is None:
        logger = logging.getLogger()
    state.CLIENT = LogClient(logger)


def add_field(name, val):
    if state.CLIENT is None:
        state.warn_uninitialized()
        return
    state.CLIENT.add_field(name, val)


def add(data):
    if state.CLIENT is None:
        state.warn_uninitialized()
        return
    state.CLIENT.add(data)


def new_event(data=None):
    return Event(data, state.CLIENT)
