import unittest
from libevent.fields import Fields


class TestFields(unittest.TestCase):
    def test_init(self):
        f = Fields()
        self.assertEqual({}, f._data)

    def test_add_field(self):
        field_key = 'a'
        field_val = 1
        f = Fields()
        f.add_field(field_key, field_val)
        self.assertEqual({field_key: field_val}, f.get_data())

    def test_add(self):
        field_map = {'a': 1, 'b': 2}
        f = Fields()
        f.add(field_map)
        self.assertEqual(field_map, f.get_data())

    def test_add_with_int(self):
        f = Fields()
        with self.assertRaises(TypeError) as context:
            f.add(17) # noqa
        self.assertEqual('add requires a dict-like argument',
                         str(context.exception))

    def test_eq(self):
        f = Fields()
        g = Fields()
        field_map = {'a': 1, 'b': 2}
        for k, v in field_map.items():
            f.add_field(k, v)
            g.add_field(k, v)
        self.assertEqual(f, g)

    def test_neq(self):
        f = Fields()
        g = Fields()
        field_map = {'a': 1, 'b': 2}
        for k, v in field_map.items():
            f.add_field(k, v)
            g.add_field(k, v + 1)
        self.assertNotEqual(f, g)

    def test_is_empty(self):
        f = Fields()
        self.assertTrue(f.is_empty())
