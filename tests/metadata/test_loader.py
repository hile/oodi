"""
Unit tests for oodi.metadata.loader module
"""
from pathlib import Path

import pytest

from oodi.exceptions import MetadataError

from ..utils import (
    validate_debug_disabled,
    validate_debug_enabled,
    validate_error_debug_disabled,
    validate_message_silent_disabled,
    validate_message_silent_enabled,
)


def test_album_metadata_files(mock_sample_library):
    """
    Test album metadata files are loaded from sample library
    """
    mock_sample_library.load()
    for album in mock_sample_library.albums.values():
        assert len(album.metadata.albumart) > 0
        assert len(album.metadata.booklets) > 0


def test_album_metadata_load_invalid_file(mock_album):
    """
    Test loading an unexpected file as album metadata
    """
    with pytest.raises(MetadataError):
        mock_album.metadata.add_metadata_file(Path(__file__))


def test_album_metadata_debug_disabled(mock_album, capsys):
    """
    Test album metadata debug method with debugging disabled
    """
    assert mock_album.library.config.__debug_enabled__ is False
    validate_debug_disabled(mock_album.metadata, capsys)


def test_album_metadata_debug_enabled(mock_album, capsys):
    """
    Test album metadata debug method with debugging enabled
    """
    mock_album.library.config.__debug_enabled__ = True
    validate_debug_enabled(mock_album.metadata, capsys)


def test_album_metadata_error_message(mock_album, capsys):
    """
    Test album metadata error method with debugging disabled
    """
    assert mock_album.library.config.__debug_enabled__ is False
    validate_error_debug_disabled(mock_album.metadata, capsys)


def test_album_metadata_message_silent_disabled(mock_album, capsys):
    """
    Test album metadata debug method with silent flag disabled
    """
    assert mock_album.library.config.__silent__ is False
    validate_message_silent_disabled(mock_album.metadata, capsys)


def test_album_metadata_message_silent_enabled(mock_album, capsys):
    """
    Test album metadata debug method with silent flag enabled
    """
    mock_album.library.config.__silent__ = True
    validate_message_silent_enabled(mock_album.metadata, capsys)
