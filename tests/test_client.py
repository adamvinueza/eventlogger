from eventlogger.logclient import LogClient
import logging
import unittest
from unittest.mock import patch


# patch the logger
class TestClient(unittest.TestCase):
    def test_init(self):
        c = LogClient()
        self.assertIsNotNone(c)

    def test_add_field(self):
        fld = {'label': True}
        c = LogClient()
        c.add_field('label', True)
        self.assertEqual(c.fields._data, fld)

    def test_add(self):
        fld = {'label': True}
        c = LogClient()
        c.add(fld)
        self.assertEqual(c.fields._data, fld)

    @patch('eventlogger.logclient.logging')
    def test_send(self, mock_logging):
        msg = "hello!"
        c = LogClient(mock_logging)
        c.send(msg, logging.INFO)
        self.assertTrue(mock_logging.log.called)
