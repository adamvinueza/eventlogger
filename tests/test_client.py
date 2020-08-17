import unittest

import eventlogger.logclient as logclient


# patch the logger
class TestClient(unittest.TestCase):
    def test_init(self):
        c = logclient.LogClient()
        self.assertIsNotNone(c)

    def test_add_field(self):
        fld = {'label': True}
        c = logclient.LogClient()
        c.add_field('label', True)
        self.assertEqual(c.fields._data, fld)

    def test_add(self):
        fld = {'label': True}
        c = logclient.LogClient()
        c.add(fld)
        self.assertEqual(c.fields._data, fld)
