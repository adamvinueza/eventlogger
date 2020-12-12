from unittest import TestCase
from unittest.mock import patch
from libevent.fields import Fields
from libevent.event import Event
import libevent
import libevent.state as state
import datetime
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
        self.assertEqual(True, state.WARNED_UNINITIALIZED)
        mock_logger.getLogger.assert_called_once()

    @patch('libevent.log_handler.logging')
    def test_send(self, mock_logger):
        libevent.init()
        evt = libevent.new_event(self.evt._fields.get_data())
        mock_logger.getLogger().level = logging.INFO
        evt.send()
        self.assertFalse(libevent.state.WARNED_UNINITIALIZED)
        mock_logger.getLogger().log.assert_called_once_with(logging.INFO,
                                                            str(evt))

    @patch('libevent.log_handler.logging.getLogger')
    def test_send_default(self, mock_get_logger):
        libevent.init()
        mock_get_logger.return_value.level = logging.INFO
        evt = libevent.new_event(self.evt._fields.get_data())
        evt.send()
        self.assertFalse(libevent.state.WARNED_UNINITIALIZED)
        mock_get_logger.return_value.log.assert_called_once_with(logging.INFO,
                                                                 str(evt))

    @patch('libevent.event.datetime')
    def test_timer(self, mock_datetime):
        def do_nothing():
            pass

        mock_datetime.datetime.utcnow = TimeFaker().fake_now
        libevent.init()
        libevent.new_event(self.evt._fields.get_data())
        evt = self.evt
        with evt.timer():
            do_nothing()
        self.assertEqual(1000, evt[libevent.event.Event.ELAPSED_MS_KEY])

    @patch('libevent.datetime')
    def test_event_chain(self, mock_datetime):
        mock_datetime.utcnow = TimeFaker().fake_now
        libevent.init()
        parent = libevent.new_event(self.evt._fields.get_data())
        child = libevent.new_event(self.evt._fields.get_data(),
                                   parent_id=parent.id)
        self.assertTrue(libevent.constants.PARENT_ID_KEY in child)
        parent_ts = parent[libevent.constants.TIMESTAMP_KEY]
        child_ts = child[libevent.constants.TIMESTAMP_KEY]
        duration = (child_ts - parent_ts).total_seconds()
        self.assertEqual(1.0, duration)
