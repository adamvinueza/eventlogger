from datetime import datetime
from unittest import TestCase
from libevent import state, LogHandler
import libevent
import os


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
        self.logfile_path = "integration_test_log.json"
        lh = LogHandler.default_handler(filename=self.logfile_path)
        libevent.init(handlers=[lh])

    def tearDown(self):
        os.remove(self.logfile_path)

    def test_init(self):
        self.assertFalse(state.WARNED_UNINITIALIZED)

    def test_send(self):
        add(1, 2)
        add(3, 4)
        self.assertTrue(os.path.exists(self.logfile_path))
        line_count = sum(1 for line in open(self.logfile_path))
        self.assertEqual(2, line_count)
