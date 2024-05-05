"""
Client for interacting with the LuxerOne Residential API.

The LuxerOneClient provides both synchronous and asynchronous implementations for each method.
"""

from typing import Optional, Union

from luxerone.api import API, api_request, async_api_request
from luxerone.auth import AuthTokenDetails, _AuthResponse
from luxerone.exceptions import RequestNotAuthenticatedException, TokenExpiredException
from luxerone.forms import (
    UpdateUserSettingsForm,
    _LoginRequestForm,
    _LogoutForm,
    _LongLivedTokenForm,
    _ResetPasswordForm,
)
from luxerone.package import HistoricalPackage, Package
from luxerone.user import UserInfo


class LuxerOneClient:
    """
    Unofficial LuxerOne Python client.

    :param username: Optional username. If one is not provided, :meth:`LuxerOneClient.login`
                     must be called manually or a token must be provided.
    :param password: The password associated with the provided username.
    :param auth_token_details: Optional parameter. If no username or password is provided,
                               an existing :class:`AuthTokenDetails` can be used.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth_token_details: Optional[AuthTokenDetails] = None,
    ):
        """
        :param username: Optional username. If one is not provided, :meth:`LuxerOneClient.login`
                         must be called manually or a token must be provided.
        :param password: The password associated with the provided username.
        :param auth_token_details: Optional parameter. If no username or password is provided,
                                an existing token can be provided.
        :raise LuxerOneAPIException: when failure to login occurs.
        """
        self._auth_token_details = None
        if username is not None and password is not None:
            self.login(username, password)
            return
        if auth_token_details is not None:
            self._auth_token_details = auth_token_details

    def login(self, username: str, password: str, ttl: int = 300) -> None:
        """
        Gets an API auth token to submit requests.

        :param username: Username
        :param password: Password
        :param ttl: Time to live for the token in seconds. Defaults to 300
                    (five minutes) with a max of 1800 (thirty minutes).
        :raise LuxerOneAPIException: when failure to login occurs.
        """
        form = _LoginRequestForm(username, password, ttl)
        login_resp = _AuthResponse(dict(api_request(api=API.AUTH, form=form)))
        self._auth_token_details = AuthTokenDetails(
            login_resp.token, ttl  # type: ignore
        )

    async def async_login(self, username: str, password: str, ttl: int = 300) -> None:
        """
        Gets an API auth token to submit requests asynchronously.

        :param username: Username
        :param password: Password
        :param ttl: Time to live for the token in seconds. Defaults to 300
                    (five minutes) with a max of 1800 (thirty minutes).
        :raise LuxerOneAPIException: when failure to login occurs.
        """
        form = _LoginRequestForm(username, password, ttl)
        login_resp = _AuthResponse(
            dict(await async_api_request(api=API.AUTH, form=form))
        )
        self._auth_token_details = AuthTokenDetails(login_resp.token, ttl)  # type: ignore

    def get_long_lived_token(self, ttl: int = 18000000) -> AuthTokenDetails:
        """
        Gets a long-lived API auth token. Must have received an auth token
        prior to making this call by either supplying your own or providing
        your login credentials to the class constructor or by calling
        :meth:`LuxerOneClient.login`.

        **Please note** that there appears to be a bug with the server-side
        logout functionality, resulting in :meth:`LuxerOneClient.logout`
        having no affect. It is not advised to create long-lived tokens as there
        is no way to invalidate them until Luxer One fixes this issue.

        One the request for the long-lived token has been processed, the
        token used by the client will be automatically
        be changed to use the new token and the prior auth token will be invalidated.

        :param ttl: time to live in seconds for the long-lived token.
                    Max value is 18000000 (208.3 days)
        :raise RequestNotAuthenticatedException: when called without having
                                                 an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: the auth token details for the long-lived-token.
        """
        self._validate_token()
        form = _LongLivedTokenForm(ttl)
        login_resp = _AuthResponse(
            dict(
                api_request(
                    API.AUTH_LONG_TERM,
                    token=self._auth_token_details.token,  # type: ignore
                    form=form,
                )
            )
        )
        # invalidate the prior token
        self.logout()
        self._auth_token_details = AuthTokenDetails(login_resp.token, ttl)  # type: ignore
        return self._auth_token_details

    async def async_get_long_lived_token(self, ttl: int = 18000000) -> AuthTokenDetails:
        """
        Asynchronously gets a long-lived API auth token. Must have received an auth token
        prior to making this call by either supplying your own or providing
        your login credentials to the class constructor or by calling
        :meth:`LuxerOneClient.login`.

        **Please note** that there appears to be a bug with the server-side
        logout functionality, resulting in :meth:`LuxerOneClient.logout`
        having no affect. It is not advised to create long-lived tokens as there
        is no way to invalidate them until Luxer One fixes this issue.

        One the request for the long-lived token has been processed, the
        token used by the client will be automatically
        be changed to use the new token and the prior auth token will be invalidated.

        :param ttl: time to live in seconds for the long-lived token.
                    Max value is 18000000 (208.3 days)
        :raise RequestNotAuthenticatedException: when called without having
                                                 an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: the auth token details for the long-lived-token.
        """
        self._validate_token()
        form = _LongLivedTokenForm(ttl)
        login_resp = _AuthResponse(
            dict(
                await async_api_request(
                    API.AUTH_LONG_TERM,
                    token=self._auth_token_details.token,  # type: ignore
                    form=form,
                )
            )
        )
        # invalidate the prior token
        await self.async_logout()
        self._auth_token_details = AuthTokenDetails(login_resp.token, ttl)  # type: ignore
        return self._auth_token_details

    def logout(self) -> Union[dict, None]:
        """
        Logout from the LuxerOne API. This will invalidate (in theory) the auth
        token that is being used by the client, so be careful when calling this
        method if you are using a long-lived token. Testing has shown that calling
        logout does not appear to invalidate the token.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :return: logout response or None if the token is already expired.
        """
        if self._auth_token_details is None:
            raise RequestNotAuthenticatedException()
        if not self._auth_token_details.is_expired():
            form = _LogoutForm(self._auth_token_details.token)
            response = dict(
                api_request(API.LOGOUT, token=self._auth_token_details.token, form=form)
            )
            # clear the token details from the client
            self._auth_token_details = None
            return response
        # clear the token details from the client
        self._auth_token_details = None
        return None

    async def async_logout(self) -> Union[dict, None]:
        """
        Asynchronously logout from the LuxerOne API. This will invalidate (in theory)
        the auth token that is being used by the client, so be careful when calling
        this method if you are using a long-lived token. Testing has shown that calling
        logout does not appear to invalidate the token.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :return: logout response or None if the token is already expired.
        """
        if self._auth_token_details is None:
            raise RequestNotAuthenticatedException()
        if not self._auth_token_details.is_expired():
            form = _LogoutForm(self._auth_token_details.token)
            response = dict(
                await async_api_request(
                    API.LOGOUT, token=self._auth_token_details.token, form=form
                )
            )
            # clear the token details from the client
            self._auth_token_details = None
            return response
        # clear the token details from the client
        self._auth_token_details = None
        return None

    @staticmethod
    def reset_password(email: str) -> None:
        """
        Requests a reset password email.

        :param email: email of the account to reset the password for.
        """
        form = _ResetPasswordForm(email)
        api_request(API.RESET_PASSWORD, form=form)

    @staticmethod
    async def async_reset_password(email: str) -> None:
        """
        Asynchronously requests a reset password email.

        :param email: email of the account to reset the password for.
        """
        form = _ResetPasswordForm(email)
        await async_api_request(API.RESET_PASSWORD, form=form)

    def get_pending_packages(self) -> list[Package]:
        """
        Gets the list of current packages that have been delivered but not picked up.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: a list of packages that are pending pickup
        """
        self._validate_token()
        response = list(
            api_request(API.PENDING_PACKAGES, token=self._auth_token_details.token)  # type: ignore
        )
        packages = []
        for pacakge_data in response:  # pylint: disable=not-an-iterable
            packages.append(Package(package_data=pacakge_data))
        return packages

    async def async_get_pending_packages(self) -> list[Package]:
        """
        Asynchronously gets the list of current packages that have been delivered but not picked up.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: a list of packages that are pending pickup
        """
        self._validate_token()
        response = list(
            await async_api_request(
                API.PENDING_PACKAGES, token=self._auth_token_details.token  # type: ignore
            )
        )
        packages = []
        for pacakge_data in response:
            packages.append(Package(package_data=pacakge_data))
        return packages

    def get_package_history(self) -> list[HistoricalPackage]:
        """
        Gets a history of all packages received includes pending packages.
        Seems to be limited to last 50.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: a list of the last 50 packages.
        """
        self._validate_token()
        response = list(
            api_request(API.PACKAGE_HISTORY, token=self._auth_token_details.token)  # type: ignore
        )
        packages = []
        for package_data in response:  # pylint: disable=not-an-iterable
            packages.append(HistoricalPackage(package_data=package_data))
        return packages

    async def async_get_package_history(self) -> list[HistoricalPackage]:
        """
        Asynchronously gets a history of all packages received includes pending packages.
        Seems to be limited to last 50.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: a list of the last 50 packages.
        """
        self._validate_token()
        response = list(
            await async_api_request(
                API.PACKAGE_HISTORY, token=self._auth_token_details.token  # type: ignore
            )
        )
        packages = []
        for pacakge_data in response:
            packages.append(HistoricalPackage(package_data=pacakge_data))
        return packages

    def get_user_info(self) -> UserInfo:
        """
        Returns a UserInfo object containing the information for the authenticated user.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: User Information.
        """
        self._validate_token()
        response = dict(
            api_request(API.USER_INFO, token=self._auth_token_details.token)  # type: ignore
        )
        return UserInfo(response)

    async def async_get_user_info(self) -> UserInfo:
        """
        Asynchronously returns a UserInfo object containing the
        information for the authenticated user.

        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :returns: User Information.
        """
        self._validate_token()
        response = dict(
            await async_api_request(
                API.USER_INFO, token=self._auth_token_details.token  # type: ignore
            )
        )
        return UserInfo(response)

    def update_user_settings(self, form: UpdateUserSettingsForm) -> dict:
        """
        Changes user settings. Keys are values from :meth:`LuxerOneClient.get_user_info`
        Not all options are changeable.

        This is still a work in progress and will eventually provide wrapper classes
        for manipulating user information.

        :param form: UpdateUserSettingsForm, any field left blank will not be modified.
        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :return: the api response.
        """
        self._validate_token()
        response = dict(
            api_request(
                API.UPDATE_USER_SETTINGS,
                token=self._auth_token_details.token,  # type: ignore
                form=form,
            )
        )
        return response

    async def async_update_user_settings(self, form: UpdateUserSettingsForm) -> dict:
        """
        Asynchronously changes user settings. Keys are values from
        :meth:`LuxerOneClient.get_user_info`
        Not all options are changeable.

        This is still a work in progress and will eventually provide wrapper classes
        for manipulating user information.

        :param form: UpdateUserSettingsForm, any field left blank will not be modified.
        :raise RequestNotAuthenticatedException: when called without having an auth token set.
        :raise TokenExpiredException: when an expired auth token is used.
        :raise LuxerOneAPIException: when the API call fails unexpectedly.
        :return: the api response.
        """
        self._validate_token()
        response = dict(
            await async_api_request(
                API.UPDATE_USER_SETTINGS,
                token=self._auth_token_details.token,  # type: ignore
                form=form,
            )
        )
        return response

    def _set_auth_token_details(self, auth_token_details: AuthTokenDetails) -> None:
        """
        Sets the AuthTokenDetails to be used by the client.
        Intended to be used for unit testing only.

        :param auth_token_details: Details to set.
        """

    def _validate_token(self) -> None:
        """
        Validates the auth token, ensuring it is not expired.

        :raise RequestNotAuthenticatedException: if called without an auth token.
        :raise TokenExpiredException: if called with an expired token.
        """
        if self._auth_token_details is None:
            raise RequestNotAuthenticatedException()
        if self._auth_token_details.is_expired():
            raise TokenExpiredException(
                "Your API Auth token expired, "
                "please login again to receive a new one."
            )

    def _is_logged_in(self) -> bool:
        """
        For unit testing purposes, checks if we are logged in.
        :return: true if logged in, else false.
        """
        try:
            self._validate_token()
        except (RequestNotAuthenticatedException, TokenExpiredException):
            return False
        return True
