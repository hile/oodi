"""
Unit tests for oodi.metadata.formats.base module
"""
from pathlib import Path
from oodi.metadata.formats.base import Metadata

from ...utils import object_rich_compare


def test_metadata_base_properties(mock_empty_config, mock_metadata_file) -> None:
    """
    Test properties of metadada base class with all valid metadata files
    """
    obj = Metadata(config=mock_empty_config, path=mock_metadata_file)
    assert isinstance(obj.__repr__(), str)


def test_metadata_base_rich_compare_same_type(mock_empty_config, tmpdir) -> None:
    """
    Test rich comparison methods of base metadata  objects of same metadata types
    """
    a = Metadata(mock_empty_config, Path(tmpdir.strpath, 'a.png'))
    b = Metadata(mock_empty_config, Path(tmpdir.strpath, 'b.jpg'))
    object_rich_compare(a, b)


def test_metadata_base_rich_compare_different_type(mock_empty_config, tmpdir) -> None:
    """
    Test rich comparison methods of base metadata objects of different metadata types
    """
    a = Metadata(mock_empty_config, Path(tmpdir.strpath, 'albumart.png'))
    b = Metadata(mock_empty_config, Path(tmpdir.strpath, 'booklet.pdf'))
    object_rich_compare(a, b)
