from unittest import TestCase
from libevent import state
from libevent.log_handler import LogHandler
from io import StringIO
import libevent
import logging
import os


def get_func_event(f, call_id=None):
    evt = libevent.new_event()
    evt.add_field('func_name', f.__name__)
    return evt


def add(x, y):
    evt = get_func_event(f=add, call_id=add.__name__)
    evt.add_field('params', {
        'x': x,
        'y': y
    })
    with evt.timer():
        result = x + y
    evt.add_field('result', result)
    evt.send()
    return result


class TestEventFileLogger(TestCase):

    def setUp(self):
        self.logfile_path = "integration_test_log.json"
        app_id = "test_event"
        lh = LogHandler.with_handler(
            name=app_id,
            handler=logging.FileHandler(filename=self.logfile_path)
        )
        libevent.init(handlers=[lh])

    def tearDown(self):
        os.remove(self.logfile_path)

    def test_init(self):
        self.assertFalse(state.WARNED_UNINITIALIZED)

    def test_send(self):
        evt = libevent.new_event()
        func = self.test_send.__name__
        evt.add_field('func_name', func)
        add(1, 2)
        add(3, 4)
        evt.send()
        self.assertTrue(os.path.exists(self.logfile_path))
        with open(self.logfile_path) as reader:
            line_count = sum(1 for line in reader)
        self.assertEqual(3, line_count)


class TestEventConsoleLogger(TestCase):

    def setUp(self):
        self.stream = StringIO()
        lh = LogHandler.with_handler(
            name="test",
            handler=logging.StreamHandler(self.stream)
        )
        libevent.init(handlers=[lh])

    def test_init(self):
        self.assertFalse(state.WARNED_UNINITIALIZED)

    def test_send(self):
        evt = libevent.new_event()
        evt.add_field('func_name', self.test_send.__name__)
        add(1, 2)
        add(3, 4)
        evt.send()
        self.stream.seek(0)
        lines = sum(1 for _ in self.stream)
        self.stream.seek(0)
        self.assertEqual(3, lines)
