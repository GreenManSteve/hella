import unittest

from api.functions.hella.get_calibration.index import handler


class TestIndex(unittest.TestCase):
    def test_handler(self):
        resp = handler({}, None)
        self.assertEqual({}, resp)
