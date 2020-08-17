'''
ADAPTED FROM Client class AT https://github.com/honeycombio/libhoney-py/
'''
import logging
from eventlogger.fields import Fields


LOGLEVELS = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]


class LogClient(object):
    '''Manages logging of events. '''
    def __init__(self, logger=None):
        if logger is None:
            logger = logging.getLogger()
        self.logger = logger
        self.fields = Fields()

    def add_field(self, name, value):
        '''Add a global field.'''
        self.fields.add_field(name, value)

    def add(self, data):
        '''Use a mappable object to add a global field.'''
        self.fields.add(data)

    def send(self, msg, level):
        '''Log the message at the specified level.'''
        if level not in LOGLEVELS:
            self.logger.warn(
                f"invalid log level: {level}, using {logging.INFO}"
            )
            level = logging.INFO
        self.logger.log(msg, level)
