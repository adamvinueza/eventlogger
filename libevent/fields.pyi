from typing import Any, Dict
"""
ADAPTED FROM FieldsHolder CLASS AT https://github.com/honeycombio/libhoney-py/
"""


class Fields:
    def __init__(self) -> None: ...
    def __add__(self, other: Any) -> Fields: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __getitem__(self, key: str) -> Any: ...
    def __contains__(self, key: str) -> bool: ...
    def add_field(self, name: str, val: Any) -> None: ...
    def add(self, data: Dict) -> None: ...
    def get_data(self) -> Dict: ...
    def is_empty(self) -> bool: ...
    def __str__(self) -> str: ...