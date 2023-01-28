"""
Unit tests for oodi.library.library module
"""
from oodi.library.tree import Library, LibraryItem

from ..conftest import (
    MOCK_WHITENOISE_SAMPLES_COUNT,
    MOCK_WHITENOISE_SAMPLES_FOLDER_COUNT
)


def test_library_loader_properties(
        mock_empty_config,
        missing_tmpdir_directory) -> None:
    """
    Test propreties of an empty Library object
    """
    assert not missing_tmpdir_directory.exists()
    obj = mock_empty_config.get_library(path=missing_tmpdir_directory)
    assert obj.config == mock_empty_config
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
    assert obj.sorted is True


def test_library_loader_sample_library_load(mock_sample_library):
    """
    Mock loading the test data directory with whitenoise samples
    """
    items = list(mock_sample_library)
    assert len(items) == MOCK_WHITENOISE_SAMPLES_COUNT + MOCK_WHITENOISE_SAMPLES_FOLDER_COUNT
    for item in items:
        if item.is_file():
            assert isinstance(item, LibraryItem)
        else:
            assert isinstance(item, Library)
