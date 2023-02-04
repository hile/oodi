"""
Unit tests for oodi.metadata.constants module
"""
from oodi.metadata.constants import (
    DEFAULT_ALBUMART_FILENAME,
    ALBUMART_FILENAME_SUFFIXES,
    ALBUMART_SUPPORTED_FILENAMES,
)


def test_metadata_constants():
    """
    Test some generated constants are consistent together
    """
    assert isinstance(DEFAULT_ALBUMART_FILENAME, str)
    assert len(ALBUMART_FILENAME_SUFFIXES) > 0
    assert len(ALBUMART_SUPPORTED_FILENAMES) > 0
    assert DEFAULT_ALBUMART_FILENAME in ALBUMART_SUPPORTED_FILENAMES
