import eventlogger.state as state
from eventlogger.event import Event

def init(logger=None):
    if logger is None:
        logger = logger.getLogger()
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
    state.add(data)

def new_event(data={}):
    return new Event(data, state.CLIENT)
