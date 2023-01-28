"""
Unit tests for oodi.configuration.loader module
"""
from oodi.configuration import Configuration


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
