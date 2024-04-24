from requests import Response
import unittest
from unittest.mock import MagicMock, patch

from luxerone.client import LuxerOneClient
from luxerone.exceptions import LuxerOneAPIException


class TestLuxerOneApiResponse(unittest.TestCase):
    async def test_async_login(self):
        mock_response = Response()
        mock_response.json = MagicMock(return_value={"data": {"token": "token-value"}})
        client = LuxerOneClient()
        with patch("luxerone.api.Session.send", return_value=mock_response):
            client.login(username="user.login", password="user.password")
        assert client._is_logged_in()

    async def test_async_login_bad_credentials(self):
        mock_response = Response()
        mock_response.json = MagicMock(return_value={"data": None, "error": "bad_auth"})
        client = LuxerOneClient()
        with patch("luxerone.api.Session.send", return_value=mock_response):
            with self.assertRaises(LuxerOneAPIException):
                client.login(username="user.login", password="user.password")


if __name__ == '__main__':
    unittest.main()
