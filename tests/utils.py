"""
Unit test validator utilities
"""
from typing import Any


def object_rich_compare(a: Any, b: Any) -> None:
    """
    Test basic rich comparison methods for two object of same type
    """
    assert a == a  # pylint: disable=comparison-with-itself
    assert a != b

    assert a < b
    assert a <= b
    assert a <= a  # pylint: disable=comparison-with-itself

    assert b > a
    assert b >= a
    assert b >= b  # pylint: disable=comparison-with-itself
