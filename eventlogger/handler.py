import abc
from eventlogger.event import Event


class Handler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def send(self, evt: Event) -> None:
        pass
