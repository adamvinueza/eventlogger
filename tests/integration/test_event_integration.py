from datetime import datetime
from unittest import TestCase
from libevent.log_handler import LogHandler
import libevent


def get_func_event(f):
    evt = libevent.new_event()
    evt.add_field('func_name', f.__name__)
    evt.add_field('timestamp', datetime.now().isoformat())
    return evt


def add(x, y):
    evt = get_func_event(add)
    evt.add_field('params', {
        'x': x,
        'y': y
    })
    with evt.timer():
        result = x + y
    evt.add_field('result', result)
    evt.send()
    return result


class TestEventIntegration(TestCase):
    def setUp(self):
        lh = LogHandler.default_handler(filename="integration_test_log.json")
        libevent.init(handlers=[lh])

    def test_send(self):
        add(1, 2)
        add(3, 4)
