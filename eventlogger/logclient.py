'''
ADAPTED FROM Client class AT https://github.com/honeycombio/libhoney-py/
'''
import logging

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

    def send(self, msg, level):
        if level not in LOGLEVELS:
            self.logger.warn(
                f"invalid log level: {level}, using {logging.INFO}"
            )
            level = logging.INFO
        self.logger.log(msg, level)
