"""Request Data models."""

# most of the classes here are just data wrappers, so disable the public method check.
# pylint: disable=too-few-public-methods

import uuid
from typing import Any, Optional


def _gen_uuid() -> str:
    """
    Generates a UUID.
    :return: a 64 bit uuid as a hex string for new clients.
    """
    generated_id = uuid.uuid4().int & (1 << 64) - 1
    return hex(generated_id)[2:]


class _RequestForm:
    def get_data(self) -> dict[str, Any]:
        """
        Gets the data as a dictionary ready for an API request.

        :return: form data as dict
        """
        return self.__dict__


class _LoginRequestForm(_RequestForm):
    """
    Login request form.

    :param username: username
    :param password: password
    :param ttl: token time to live in seconds
    """

    def __init__(self, username: str, password: str, ttl: int):
        """
        :param username: username
        :param password: password
        :param ttl: token time to live in seconds.
        """
        self.username = username
        self.password = password
        self.expires = ttl
        self.uuid = _gen_uuid()
        self.remember = True

    def get_data(self) -> dict[str, Any]:
        """
        Gets the data as a dictionary ready for an API request.

        :return: form data as dict
        """
        data = {"as": "token"}
        for key, value in self.__dict__.items():
            data[key] = value
        return data


class _LongLivedTokenForm(_RequestForm):
    """
    Long-lived token request form.

    :param ttl: token time to live in seconds.
    """

    def __init__(self, ttl: int):
        """:param ttl: token time to live in seconds."""
        self.ttl = ttl

    def get_data(self) -> dict[str, Any]:
        """
        Gets the data as a dictionary ready for an API request.

        :return: form data as dict
        """
        data = {"expires": self.ttl, "as": "token"}
        return data


class _LogoutForm(_RequestForm):
    """
    Logout request form.

    :param token: token to expire
    """

    def __init__(self, token: str):
        """:param token: token to expire."""
        self.revoke = token


class _ResetPasswordForm(_RequestForm):
    """
    Reset password request form.

    :param email: email of the account to reset the password for.
    """

    def __init__(self, email: str):
        """:param email: email of the account to reset the password for."""
        self.email = email


class UpdateUserSettingsForm(_RequestForm):
    # disable invalid name check as the camel case is required.
    # pylint: disable=invalid-name
    # disable the check for too many instance attributes as this represents data from api call.
    # pylint: disable=too-many-instance-attributes
    # disable too many arguments as this takes in the api response as is.
    # pylint: disable=too-many-arguments
    """Update user settings form."""

    def __init__(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        secondary_email: Optional[str] = None,
        allow_emails: Optional[bool] = None,
        allow_sms: Optional[bool] = None,
        allow_push_notifications: Optional[bool] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.secondaryEmail = secondary_email
        self.allowEmails = allow_emails
        self.allowSms = allow_sms
        self.allowPushNotifications = allow_push_notifications

    def get_data(self) -> dict[str, Any]:
        data = {}
        for key, value in self.__dict__.items():
            if value is not None:
                data[key] = value
        return data
