"""
Unit tests for oodi.codecs.formats.base module
"""
from oodi.codecs.formats.base import Codec


def test_codecs_formats_base_properties(mock_empty_config):
    """
    Test properties of the Codec base class
    """
    obj = Codec(mock_empty_config)
    assert obj.match_file_properties(mock_empty_config.__path__) is True
    # Base codec has no suffixes defined and this always returns False
    assert obj.match_file(mock_empty_config.__path__) is False
