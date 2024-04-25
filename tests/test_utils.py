"""Utility function testing."""

import unittest

from luxerone._utils import _populate_self


class TestObject:
    """Test object/data wrapper."""

    def __init__(self):
        self.name = None
        self.data = None


class TestUtilities(unittest.TestCase):
    """Test case for the luxerone._utilities module."""

    def test_populate_self_populates(self):
        """Test to ensure object fields are populated correctly from data."""

        data = {"name": "test", "data": "value"}
        target = TestObject()
        _populate_self(target, data)
        self.assertEqual(target.name, "test")  # add assertion here
        self.assertEqual(target.data, "value")

    def test_populate_self_populates_unknowns_with_none(self):
        """Test to ensure that unknown fields are populated with None."""

        data = {"name": "test"}
        target = TestObject()
        _populate_self(target, data)
        self.assertEqual(target.name, "test")  # add assertion here
        self.assertEqual(target.data, None)


if __name__ == "__main__":
    unittest.main()
