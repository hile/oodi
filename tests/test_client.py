"""
Unit tests for oodi.client library
"""
from oodi.client import Oodi
from oodi.configuration import Configuration


def test_client_oodi_properties(mock_empty_config_file) -> None:
    """
    Test loading oodi.client.iClient object with empty configuration
    """
    client = Oodi()
    assert client.__debug_enabled__ is False
    assert client.__silent__ is False
    assert isinstance(client.config, Configuration)
    assert client.config.__path__.parent == mock_empty_config_file
