from unittest import TestCase
from io import StringIO
from libevent.event import Event
from libevent.fields import Fields
from libevent.stdout_handler import StdoutHandler
import sys


class TestStdoutHandler(TestCase):
    def setUp(self):
        self.stream = StringIO()
        sys.stdout = self.stream

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_send(self):
        data = {'field1': 'value1'}
        fields = Fields()
        fields.add_field('field2', 'value2')
        evt = Event(data, fields)
        sh = StdoutHandler()
        sh.send(evt)
        self.stream.seek(0)
        lines = sum(1 for _ in self.stream)
        self.stream.seek(0)
        self.assertEqual(1, lines)

