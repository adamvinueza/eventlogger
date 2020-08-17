import unittest
import os


class TestFirst(unittest.TestCase):
    def test_first(self):
        print(os.getcwd())
