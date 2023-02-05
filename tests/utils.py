"""
Unit test validator utilities
"""
from typing import Any

MOCK_MESSAGE = 'Test message'


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


def validate_debug_disabled(obj: Any, capsys) -> None:
    """
    Validate debug disabled flag suppesses any debug messages
    """
    obj.debug(MOCK_MESSAGE)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''


def validate_debug_enabled(obj: Any, capsys) -> None:
    """
    Validate debug enabled flag does not suppress debug messages
    """
    obj.debug(MOCK_MESSAGE)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err.splitlines() == [MOCK_MESSAGE]


def validate_error_debug_disabled(obj: Any, capsys) -> None:
    """
    Validate debug disabled flag does not suppress error messages
    """
    obj.error(MOCK_MESSAGE)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err.splitlines() == [MOCK_MESSAGE]


def validate_message_silent_disabled(obj: Any, capsys) -> None:
    """
    Validate silent disabled flag does not suppress normal messages
    """
    obj.message(MOCK_MESSAGE)
    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out.splitlines() == [MOCK_MESSAGE]


def validate_message_silent_enabled(obj: Any, capsys) -> None:
    """
    Validate silent enabled flag suppresses normal messages
    """
    obj.message(MOCK_MESSAGE)
    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''
