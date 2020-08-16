import json
from contextlib import ContextManager
from eventlogger import Fields
'''
ADAPTED FROM Event CLASS AT https://github.com/honeycombio/libhoney-py
'''

class Event(object):
    '''A collection of fields to be logged.'''
    def __init__(self, data={}, fields=Fields(), client=None):
        self.client = client
        self._fields = Fields()
        if self.client:
            self._fields += self.client.fields
        self._fields.add(data)
        self._fields += fields

    def add_field(self, key, value, err_on_key_exists=False):
        self.add({key: value}, err_on_key_exists)

    def add(self, data, err_on_key_exists=False):
        for k, v in data.items():
            if k in self.items and err_on_key_exists:
                raise ValueError(f"event field {k} exists")
        self.items.update(data)

    def send(self, level=logging.INFO):
        if self.client is None:
            state.warn_uninitialized()
            return
        self.client.send(self, level)

    @contextmanager
    def timer(self, name='elapsed_ms'):
        start = datetime.datetime.now()
        yield
        duration = datetime.datetime.now() - start
        self.add_field(name, duration.total_seconds() * 1000)

    def __str__(self):
        return str(self._fields)
