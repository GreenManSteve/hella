import unittest

from api.functions.hella.health_check.index import handler


class TestIndex(unittest.TestCase):
    def test_handler(self) -> None:
        """
        Tests that the health check handler returns a consistent body and status code
        and that the Content-Type is consistent.
        :return:
        """
        actual = handler({}, None)
        expected = {
            "statusCode": 200,
            "body": "ok",
            "headers": {"Content-Type": "application/json"},
        }

        self.assertEqual(expected, actual)
