"""
Unit tests for oodi.configuration.loader module
"""
import pytest

from oodi.metadata.constants import ALBUMART_SUPPORTED_FILENAMES

from ..conftest import MOCK_DATA

MOCK_METADATA = MOCK_DATA.joinpath('metadata')

MOCK_METADATA_FILES = [path for path in MOCK_METADATA.glob('**/*') if path.is_file()]
MOCK_ALBUMART_FILES = [
    path
    for path in MOCK_METADATA_FILES
    if path.name in ALBUMART_SUPPORTED_FILENAMES
]


@pytest.fixture(params=MOCK_METADATA_FILES)
def mock_metadata_file(request):
    """
    Mock fixture to list all available metadata files in test data
    """
    yield request.param


@pytest.fixture(params=MOCK_ALBUMART_FILES)
def mock_albumart_file(request):
    """
    Mock fixture to list all available album art files in test data
    """
    yield request.param
