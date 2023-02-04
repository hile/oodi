"""
Unit tests for oodi.metadata.constants module
"""
from oodi.metadata.constants import (
    ALBUMART_FILENAME_SUFFIXES,
    ALBUMART_SUPPORTED_FILENAMES,
    BOOKLET_FILENAME_SUFFIXES,
    BOOKLET_SUPPORTED_FILENAMES,
    DEFAULT_ALBUMART_FILENAME,
    DEFAULT_BOOKLET_FILENAME,
)


def test_metadata_constants_albumart():
    """
    Test some generated constants are consistent together
    """
    assert isinstance(DEFAULT_ALBUMART_FILENAME, str)
    assert len(ALBUMART_FILENAME_SUFFIXES) > 0
    assert len(ALBUMART_SUPPORTED_FILENAMES) > 0
    assert DEFAULT_ALBUMART_FILENAME in ALBUMART_SUPPORTED_FILENAMES


def test_metadata_constants_booklet():
    """
    Test some generated constants are consistent together
    """
    assert isinstance(DEFAULT_BOOKLET_FILENAME, str)
    assert len(BOOKLET_FILENAME_SUFFIXES) > 0
    assert len(BOOKLET_SUPPORTED_FILENAMES) > 0
    assert DEFAULT_BOOKLET_FILENAME in BOOKLET_SUPPORTED_FILENAMES
