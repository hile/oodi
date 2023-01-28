"""
Unit tests for oodi.library.library module
"""
from oodi.library.tree import Library


def test_library_loader_properties(
        mock_empty_config,
        missing_tmpdir_directory) -> None:
    """
    Test propreties of an empty Library object
    """
    assert not missing_tmpdir_directory.exists()
    obj = mock_empty_config.get_library(path=missing_tmpdir_directory)
    assert isinstance(obj, Library)
    assert not missing_tmpdir_directory.exists()


def test_library_loader_create_missing_directory(
        mock_empty_config,
        missing_tmpdir_directory) -> None:
    """
    Test propreties of an empty Library with 'create_missing', creating the missing
    target directory
    """
    assert not missing_tmpdir_directory.exists()
    obj = mock_empty_config.get_library(path=missing_tmpdir_directory, create_missing=True)
    assert isinstance(obj, Library)
    assert missing_tmpdir_directory.exists()
