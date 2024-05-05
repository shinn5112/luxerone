"""Wrapper classes for all information relating to package deliveries."""

import json

from luxerone._utils import _populate_self

# This module represents API objects, so disable checks for too few public methods,
# too many instance attributes, and invalid names.

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=invalid-name


class Locker:
    """Locker information."""

    def __init__(self, package_data: dict):
        """:param package_data: package data in json format from the API."""
        self.lockerId = None
        self.lockerNumber = None
        self.lockerTypeId = None
        self.lockerType = None
        _populate_self(self, package_data)

    def __str__(self) -> str:
        """
        Creates a string representation of the object.

        :return: object string representation.
        """
        return json.dumps(self)


class PackageCarrier:
    """Carrier information."""

    def __init__(self, package_data: dict):
        """:param package_data: package data in json format from the API."""
        self.carrier = None
        self.carrierLogo = None
        self.trackingNumber = None
        _populate_self(self, package_data)

    def __str__(self):
        """
        Creates a string representation of the object.

        :return: object string representation.
        """
        return json.dumps(self)


class DeliveryLocation:
    """Location information regarding the package delivery location."""

    def __init__(self, package_data: dict):
        """:param package_data: package data in json format from the API."""
        self.location = None
        self.locationId = None
        self.locationAddress = None
        self.lockerLocation = None
        self.timezoneOffset = None
        _populate_self(self, package_data)

    def __str__(self):
        """
        Creates a string representation of the object.

        :return: object string representation.
        """
        return json.dumps(self)


class Package:
    """Package information."""

    def __init__(self, package_data: dict):
        """:param package_data: package data in json format from the API."""
        self.id = None
        self.deliveryTypeId = None
        self.delivered = None
        self.pickedup = None
        self.holdUntil = None
        self.accessCode = None
        self.isPerishable = False
        self.status = None
        self.charge = None
        self.pickupToken = None
        self.labels = None
        _populate_self(self, package_data)
        self.carrier = PackageCarrier(package_data)
        self.locker = Locker(package_data)
        self.location = DeliveryLocation(package_data)

    def __str__(self):
        """
        Creates a string representation of the object.

        :return: object string representation.
        """
        return json.dumps(self)


class HistoricalPackage(Package):
    """Historical Package information."""

    def __init__(self, package_data: dict):
        """:param package_data: package data in json format from the API."""
        super().__init__(package_data)
        try:
            self.resident = package_data["resident"]
        except KeyError:
            self.resident = None
        try:
            self.signature = package_data["signature"]
        except KeyError:
            self.signature = None

    def __str__(self):
        """
        Creates a string representation of the object.

        :return: object string representation.
        """
        return json.dumps(self)
