from unittest import TestCase
from unittest.mock import patch
from libevent.event import Event
from libevent.fields import Fields
import datetime
import libevent.state
import logging


class TimeFaker(object):
    mock_date = dict(year=2020, month=1, day=1, hour=1, minute=1)

    def __init__(self):
        self.seconds = 0

    def fake_now(self):
        fake_time = datetime.datetime(TimeFaker.mock_date['year'],
                                      TimeFaker.mock_date['month'],
                                      TimeFaker.mock_date['day'],
                                      TimeFaker.mock_date['hour'],
                                      TimeFaker.mock_date['minute'],
                                      self.seconds)

        self.seconds += 1
        return fake_time


class TestEvent(TestCase):

    def setUp(self):
        self.data = {'field1': 'value1'}
        fields = Fields()
        fields.add_field('field2', 'value2')
        self.fields = fields
        self.evt = Event(self.data, self.fields)

    def test_init(self):
        evt = self.evt
        expected = {**self.data, **evt._fields.get_data()}
        assert(evt is not None)
        assert(expected == evt._fields.get_data())

    def test_add_field(self):
        evt = self.evt
        added = {"field3": "value3"}
        expected = {**evt._fields.get_data(), **added}
        evt.add_field("field3", "value3")
        assert(expected == evt._fields.get_data())

    def test_add(self):
        evt = self.evt
        added = {"field3": "value3"}
        expected = {**evt._fields.get_data(), **added}
        evt.add(added)
        assert(expected == evt._fields.get_data())

    @patch('libevent.state.logging')
    def test_send_uninitialized(self, mock_logger):
        evt = self.evt
        evt.send()
        self.assertEqual(True, libevent.state.WARNED_UNINITIALIZED)
        mock_logger.getLogger.assert_called_once()

    @patch('libevent.log_handler.logging')
    def test_send(self, mock_logger):
        libevent.init()
        evt = libevent.new_event(self.evt._fields.get_data())
        evt.add_field(libevent.fields.LOG_LEVEL, logging.INFO)
        evt.send()
        self.assertFalse(libevent.state.WARNED_UNINITIALIZED)
        mock_logger.getLogger().log.assert_called_once_with(logging.INFO,
                                                            str(evt))

    @patch('libevent.log_handler.logging.getLogger')
    def test_send_warn(self, mock_logging):
        libevent.init()
        evt = libevent.new_event(self.evt._fields.get_data())
        evt.add_field(libevent.fields.LOG_LEVEL, logging.WARN)
        evt.send()
        self.assertFalse(libevent.state.WARNED_UNINITIALIZED)
        mock_logging.return_value.log.assert_called_once_with(logging.WARN,
                                                              str(evt))

    @patch('libevent.log_handler.logging.getLogger')
    @patch('libevent.log_handler.logging')
    def test_send_default(self, mock_logging, mock_get_logger):
        mock_logging.INFO = logging.INFO
        libevent.init()
        evt = libevent.new_event(self.evt._fields.get_data())
        evt.send()
        self.assertFalse(libevent.state.WARNED_UNINITIALIZED)
        mock_get_logger.return_value.log.assert_called_once_with(logging.INFO,
                                                                 str(evt))

    @patch('libevent.event.datetime')
    def test_timer(self, mock_datetime):
        def do_nothing():
            pass

        mock_datetime.datetime.now = TimeFaker().fake_now
        libevent.init()
        libevent.new_event(self.evt._fields.get_data())
        evt = self.evt
        with evt.timer():
            do_nothing()
        self.assertEqual(1000, evt[libevent.event.Event.ELAPSED_MS_KEY])
