"""
Unit test configuration specific to oodi.library module
"""
from pathlib import Path
from typing import Iterator

import pytest

from oodi.library.album import Album

TEST_ALBUM_PATHS = (
    Path('Album/In Library'),
)


@pytest.fixture(params=TEST_ALBUM_PATHS)
def mock_album_relative_path(request) -> Iterator[Path]:
    """
    Return iterator for valid album relative paths
    """
    yield request.param


# pylint: disable=redefined-outer-name
@pytest.fixture
def mock_album(mock_empty_library, mock_album_relative_path) -> Iterator[Album]:
    """
    Return mocked Album object
    """
    yield Album(mock_empty_library, mock_empty_library.joinpath(mock_album_relative_path))
