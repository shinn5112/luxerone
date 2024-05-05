"""Auth Module."""

import datetime
import json

from luxerone._utils import _populate_self

# pylint: disable=too-few-public-methods


class _AuthResponse:
    """API Login Response data wrapper."""

    def __init__(self, data: dict) -> None:
        self.token = None
        _populate_self(self, data)
        if self.token is None:
            raise ValueError("Received a token with value None")


class AuthTokenDetails:
    """
    Abstraction layer for working with token details.

    :param token: auth token.
    :param ttl: time to live in seconds.
    """

    def __init__(self, token: str, ttl: int):
        """
        :param token: auth token.
        :param ttl: time to live in seconds.
        """
        self.token = token
        self.expires_at = datetime.timedelta(seconds=ttl) + datetime.datetime.now()

    def is_expired(self) -> bool:
        """
        Whether the token has expired.

        :return: true if expired, else false.
        """
        return datetime.datetime.now() > self.expires_at

    def __str__(self) -> str:
        """
        Creates a string representation of the object.

        :return: object string representation.
        """
        return json.dumps(self)
