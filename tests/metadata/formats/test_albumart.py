"""
Unit tests for oodi.metadata.formats module
"""
from oodi.metadata.formats.albumart import AlbumArt


def test_metadata_albumart_properties(mock_empty_config, mock_albumart_file):
    """
    Unit test for basic properties of an AlbumArt object
    """
    obj = AlbumArt(mock_empty_config, mock_albumart_file)
    assert isinstance(obj.__repr__(), str)
