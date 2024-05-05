"""API specific exceptions."""


class LuxerOneAPIException(Exception):
    """Is thrown when an API error is encountered."""


class TokenExpiredException(Exception):
    """Is thrown when a request is made using an expired API auth token."""


class RequestNotAuthenticatedException(Exception):
    """Is thrown when a request is made without an API auth token."""

    def __init__(self):
        default_message = (
            "TYou have not received an API Auth token yet, login to get one."
        )
        super().__init__(default_message)
