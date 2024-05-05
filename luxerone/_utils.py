"""Utilities Module."""

import logging

_logger = logging.getLogger(__name__)


def _populate_self(obj: object, data: dict) -> None:
    """
    Convince method for populating a data wrapper from a dictionary.
    :param obj: object to populate
    :param data: data to populate from
    :return:
    """
    for key in obj.__dict__:
        try:
            setattr(obj, key, data[key])
        except KeyError:
            _logger.debug("Could not find key {}, setting value as None", key)
            setattr(obj, key, None)
