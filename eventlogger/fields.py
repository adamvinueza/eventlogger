import json
import json_handler
'''
ADAPTED FROM FieldsHolder CLASS AT https://github.com/honeycombio/libhoney-py/
'''


class Fields:
    '''A field that can be logged.'''
    def __init__(self):
        self._data = {}

    def __add__(self, other):
        self._data.update(other._data)
        return self

    def __eq__(self, other):
        return self._data == other._data

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_field(self, name, val):
        self._data[name] = val

    def add(self, data):
        try:
            for k, v in data.items():
                self.add_field(k, v)
        except AttributeError:
            raise TypeError("add requires a dict-like argument")

    def is_empty(self):
        return len(self._data) == 0

    def __str__(self):
        return json.dumps(self._data, default=json_handler.default)
