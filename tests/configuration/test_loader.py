"""
Unit tests for oodi.configuration.loader module
"""
import pytest

from oodi.codecs.formats.base import Codec
from oodi.configuration import Configuration
from oodi.exceptions import ConfigurationError

UNEXPECTED_CODEC_FORMAT = 'txt'


def test_configuration_loader_no_config_directory(mock_missing_config_file) -> None:
    """
    Test initializing oodi configuration loader when the
    configuration directory does not exist
    """
    config = Configuration()
    assert not config.__path__.is_file()
    mock_missing_config_file.mkdir(parents=True)


def test_configuration_loader_empty_config(mock_empty_config_file) -> None:
    """
    Test initializing oodi configuration loader when the configuration file
    is an empty yaml configuration file from mocked test data
    """
    config = Configuration()
    assert mock_empty_config_file.is_dir()
    assert config.__path__.is_file()


def test_configuration_loader_defaultconfig(mock_default_config_file) -> None:
    """
    Test initializing oodi configuration loader when the configuration file
    is default yaml configuration file with setings from mocked test data
    """
    config = Configuration()
    assert mock_default_config_file.is_dir()
    assert config.__path__.is_file()


# pylint: disable=unused-argument
def test_configuration_loader_get_codec_no_value(mock_empty_config_file) -> None:
    """
    Test fetching codecs by None as codec format value
    """
    assert Configuration().get_codec(None) is None


# pylint: disable=unused-argument
def test_configuration_loader_get_codec_invalid_value_type(mock_empty_config_file) -> None:
    """
    Test fetching codecs by unexpected value type for codec format
    """
    with pytest.raises(ConfigurationError):
        Configuration().get_codec(0)


# pylint: disable=unused-argument
def test_configuration_loader_get_codec_invalid_value(mock_empty_config_file) -> None:
    """
    Test fetching codecs by invalid codec format
    """
    with pytest.raises(ConfigurationError):
        Configuration().get_codec(UNEXPECTED_CODEC_FORMAT)


# pylint: disable=unused-argument
def test_configuration_loader_get_codec_valid_formats(mock_empty_config_file, valid_codec_format) -> None:
    """
    Test fetching codecs by known CodecFormat objects
    """
    assert isinstance(Configuration().get_codec(valid_codec_format), Codec)


# pylint: disable=unused-argument
def test_configuration_loader_get_codec_valid_format_names(mock_empty_config_file, valid_codec_format_name) -> None:
    """
    Test fetching codecs by known CodecFormat objects referenced by value (str)
    """
    assert isinstance(Configuration().get_codec(valid_codec_format_name), Codec)
