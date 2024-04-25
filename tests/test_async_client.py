"""Unit tests for all asynchronous client methods."""
import unittest
from unittest.mock import MagicMock, patch
from requests import Response
from luxerone.client import LuxerOneClient
from luxerone.exceptions import LuxerOneAPIException


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    """Test class."""
    async def test_async_login(self):
        """Test a valid login."""
        mock_response = Response()
        mock_response.json = MagicMock(return_value={"data": {"token": "token-value"}})
        client = LuxerOneClient()
        with patch("luxerone.api.Session.send", return_value=mock_response):
            await client.async_login(username="user.login", password="user.password")
        assert client._is_logged_in()

    async def test_async_login_bad_credentials(self):
        """Test an invalid login."""
        mock_response = Response()
        mock_response.json = MagicMock(return_value={"data": None, "error": "bad_auth"})
        client = LuxerOneClient()
        with patch("luxerone.api.Session.send", return_value=mock_response):
            with self.assertRaises(LuxerOneAPIException):
                await client.async_login(username="user.login", password="user.password")


if __name__ == '__main__':
    unittest.main()
