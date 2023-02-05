"""
Unit tests for oodi.library.library module
"""
from pathlib import Path
import os
import pytest

from oodi.exceptions import ConfigurationError
from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats.base import Codec
from oodi.library.tree import Library, LibraryItem

from ..conftest import (
    MOCK_WHITENOISE_SAMPLES_COUNT,
    MOCK_WHITENOISE_SAMPLES_FOLDER_COUNT,
    MOCK_METADATA_FILES_COUNT
)
from ..utils import (
    validate_debug_disabled,
    validate_debug_enabled,
    validate_error_debug_disabled,
    validate_message_silent_disabled,
    validate_message_silent_enabled,
)


def test_library_loader_properties(
        oodi_empty_client,
        missing_tmpdir_directory) -> None:
    """
    Test propreties of an empty Library object
    """
    assert not missing_tmpdir_directory.exists()
    obj = oodi_empty_client.get_library(path=missing_tmpdir_directory)
    assert obj.config == oodi_empty_client.config
    assert isinstance(obj, Library)
    assert not missing_tmpdir_directory.exists()

    assert isinstance(obj.codecs.default, Codec)
    assert isinstance(obj.codecs.formats, list)
    for item in obj.codecs.formats:
        assert isinstance(item, Codec)
    assert isinstance(obj.codecs.suffixes, list)
    for suffix in obj.codecs.suffixes:
        assert isinstance(suffix, str)
        assert suffix != ''
        assert suffix[0] == '.'


def test_library_loader_conflicting_codec_formats(
        oodi_empty_client,
        missing_tmpdir_directory) -> None:
    """
    Test loading a library with valid set of codec formats but with a default
    codec that is not included in the list of specified codec formats
    """
    codec_formats = [CodecFormat.OPUS.value, CodecFormat.VORBIS.value]
    with pytest.raises(ConfigurationError):
        oodi_empty_client.get_library(
            path=missing_tmpdir_directory,
            default_format=CodecFormat.MP3.value,
            formats=codec_formats,
        )


def test_library_loader_valid_codec_formats(
        oodi_empty_client,
        missing_tmpdir_directory) -> None:
    """
    Test loading a library with valid set of codec formats
    """
    codec_formats = [CodecFormat.OPUS.value, CodecFormat.VORBIS.value]
    obj = oodi_empty_client.get_library(
        path=missing_tmpdir_directory,
        default_format=CodecFormat.OPUS.value,
        formats=codec_formats,
    )
    assert obj.codecs.default.codec_format == CodecFormat.OPUS
    for codec in obj.codecs.formats:
        assert codec.codec_format.value in codec_formats


def test_library_loader_create_missing_directory(
        oodi_empty_client,
        missing_tmpdir_directory) -> None:
    """
    Test propreties of an empty Library with 'create_missing', creating the missing
    target directory
    """
    assert not missing_tmpdir_directory.exists()
    obj = oodi_empty_client.get_library(path=missing_tmpdir_directory, create_missing=True)
    assert isinstance(obj, Library)
    assert missing_tmpdir_directory.exists()
    assert obj.sorted is True


def test_library_loader_sample_library_load(mock_sample_library) -> None:
    """
    Mock loading the test data directory with whitenoise samples
    """
    mock_sample_library.load()
    items = list(mock_sample_library)
    assert len(items) == MOCK_WHITENOISE_SAMPLES_COUNT + \
        MOCK_WHITENOISE_SAMPLES_FOLDER_COUNT + \
        MOCK_METADATA_FILES_COUNT
    for item in items:
        if item.is_file():
            assert isinstance(item, LibraryItem)
        else:
            assert isinstance(item, Library)
            assert item.library == mock_sample_library

    assert len(mock_sample_library.audio_files) == MOCK_WHITENOISE_SAMPLES_COUNT


def test_library_loader_sample_library_relative_path(mock_sample_library) -> None:
    """
    Mock loading the test data directory with whitenoise samples
    """
    assert mock_sample_library.library_relative_path is None
    items = list(mock_sample_library)
    for item in items:
        if item.is_dir():
            assert isinstance(item.library_relative_path, Path)


def test_library_loader_resolve(mock_sample_library) -> None:
    """
    Test that resolve() method of Library object returns a library object
    with a full resolved path
    """
    cloned = mock_sample_library.resolve()
    assert str(cloned).startswith(os.sep)
    assert mock_sample_library.albums == cloned.albums
    assert mock_sample_library.__items__ == cloned.__items__


def test_library_debug_disabled(mock_sample_library, capsys):
    """
    Test library debug method with debugging disabled
    """
    assert mock_sample_library.config.__debug_enabled__ is False
    validate_debug_disabled(mock_sample_library, capsys)


def test_library_debug_enabled(mock_sample_library, capsys):
    """
    Test library debug method with debugging enabled
    """
    mock_sample_library.config.__debug_enabled__ = True
    validate_debug_enabled(mock_sample_library, capsys)


def test_library_error_message(mock_sample_library, capsys):
    """
    Test library error method with debugging disabled
    """
    assert mock_sample_library.config.__debug_enabled__ is False
    validate_error_debug_disabled(mock_sample_library, capsys)


def test_library_message_silent_disabled(mock_sample_library, capsys):
    """
    Test library debug method with silent flag disabled
    """
    assert mock_sample_library.config.__silent__ is False
    validate_message_silent_disabled(mock_sample_library, capsys)


def test_library_message_silent_enabled(mock_sample_library, capsys):
    """
    Test library debug method with silent flag enabled
    """
    mock_sample_library.config.__silent__ = True
    validate_message_silent_enabled(mock_sample_library, capsys)