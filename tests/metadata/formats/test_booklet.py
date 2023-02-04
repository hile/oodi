"""
Unit tests for oodi.metadata.formats.booklet module
"""
from oodi.metadata.formats.booklet import Booklet


def test_metadata_booklet_properties(mock_empty_config, mock_booklet_file):
    """
    Unit test for basic properties of an Booklet object
    """
    obj = Booklet(mock_empty_config, mock_booklet_file)
    assert isinstance(obj.__repr__(), str)
