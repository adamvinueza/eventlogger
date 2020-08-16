import unittest

import eventlogger.logclient as logclient


# patch the logger
class TestClient(unittest.TestCase):
    def test_init(self):
        c = logclient.LogClient()
        self.assertIsNotNone(c)
