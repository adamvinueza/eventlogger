import abc
from typing import Any


class Handler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def send(self, evt: Any) -> None:
        """Sends the supplied event.
        Strictly, anything can be an event. It is the responsibility of the
        event being sent to be appropriately serializable."""
        pass
