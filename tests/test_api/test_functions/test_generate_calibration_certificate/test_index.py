import unittest

from api.functions.hella.generate_calibration_certificate.index import handler


class TestIndex(unittest.TestCase):
    def test_handler(self) -> None:
        actual = handler({}, None)
        expected = {}
        self.assertEqual(expected, actual)
