from __future__ import annotations
import json
from typing import Any, Dict
import eventlogger.json_serializer as json_serializer
"""
ADAPTED FROM FieldsHolder CLASS AT https://github.com/honeycombio/libhoney-py/
"""

ERROR = "error"
LOG_LEVEL = "logLevel"


class Fields:
    """A field that can be logged."""
    def __init__(self):
        self._data = {}

    def __add__(self, other: Fields) -> Fields:
        self._data.update(other.get_data())
        return self

    def __eq__(self, other: Fields) -> bool:
        return self._data == other.get_data()

    def __ne__(self, other: Fields) -> bool:
        return not self.__eq__(other)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def add_field(self, name: str, val: Any) -> None:
        self._data[name] = val

    def add(self, data: Dict) -> None:
        try:
            for k, v in data.items():
                self.add_field(k, v)
        except AttributeError:
            raise TypeError("add requires a dict-like argument")

    def get_data(self) -> Dict:
        return self._data

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __str__(self) -> str:
        return json.dumps(self._data, default=json_serializer.default)
