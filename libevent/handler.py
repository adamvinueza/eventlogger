from typing import Any, Protocol
from libevent.fields import Fields


class Handler(Protocol):

    fields: Fields

    def send(self, evt: Any) -> None:
        """Sends the supplied event.
        Strictly, anything can be an event. It is the responsibility of the
        event being sent to be appropriately serializable."""
        pass
