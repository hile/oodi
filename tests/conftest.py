"""
Pytest unit test configuration for oodi
"""
from pathlib import Path
from shutil import rmtree
from typing import Iterator

import pytest

from oodi.client import Oodi
from oodi.configuration import Configuration
from oodi.library.tree import Library

MOCK_DATA = Path(__file__).parent.joinpath('mock')
MOCK_CONFIG_DIRECTORY = MOCK_DATA.joinpath('config/default')
MOCK_EMPTY_CONFIG_DIRECTORY = MOCK_DATA.joinpath('config/empty')

# Directory with whitenoise samples
MOCK_WHITENOISE_SAMPLES_PATH = MOCK_DATA.joinpath('samples')
MOCK_WHITENOISE_SAMPLES_FOLDER_COUNT = 2
MOCK_WHITENOISE_SAMPLES_COUNT = 9

# List of all sample files as standard Path objects from the test data directory
WHITENOISE_SAMPLE_FILES = [
    item
    for item in list(MOCK_WHITENOISE_SAMPLES_PATH.glob('**/*'))
    if item.is_file()
]


@pytest.fixture
def mock_missing_config_file(monkeypatch, tmpdir) -> Iterator[Path]:
    """
    Return a non-existing temporary directory for constant
    oodi.constants.USER_CONFIG_DIRECTORY
    """
    missing_config_path = Path(tmpdir.strpath, 'missing-userconfig')
    monkeypatch.setattr(
        'oodi.constants.USER_CONFIG_DIRECTORY',
        missing_config_path
    )
    yield missing_config_path
    if missing_config_path and missing_config_path.is_dir():
        rmtree(missing_config_path)


@pytest.fixture
def mock_empty_config_file(monkeypatch) -> Iterator[Path]:
    """
    Mock constant oodi.constants.USER_CONFIG_DIRECTORY to return
    mocked directory tests/mock/config/empty with valid but empty
    configuration file
    """
    monkeypatch.setattr(
        'oodi.constants.USER_CONFIG_DIRECTORY',
        MOCK_EMPTY_CONFIG_DIRECTORY,
    )
    yield MOCK_EMPTY_CONFIG_DIRECTORY


@pytest.fixture
def mock_default_config_file(monkeypatch) -> Iterator[Path]:
    """
    Mock constant oodi.constants.USER_CONFIG_DIRECTORY to return
    mocked directory tests/mock/config/default
    """
    monkeypatch.setattr(
        'oodi.constants.USER_CONFIG_DIRECTORY',
        MOCK_CONFIG_DIRECTORY,
    )
    yield MOCK_CONFIG_DIRECTORY


@pytest.fixture
def missing_tmpdir_directory(tmpdir) -> Iterator[Path]:
    """
    Yield missing temporary directory path for unit tests
    """
    missing_directory = Path(tmpdir.strpath, 'missing-directory')
    yield missing_directory
    if missing_directory and missing_directory.is_dir():
        rmtree(missing_directory)


# pylint: disable=redefined-outer-name,unused-argument
@pytest.fixture
def mock_empty_config(mock_empty_config_file) -> Iterator[Configuration]:
    """
    Mock returning Configuration object with mock_empty_config_file fixture
    """
    yield Configuration()


@pytest.fixture(params=WHITENOISE_SAMPLE_FILES)
def mock_sample_file(request) -> Iterator[Path]:
    """
    Mock request with full paths to the sample files in test data
    """
    yield request.param


@pytest.fixture
def mock_sample_library(mock_empty_config) -> Iterator[Library]:
    """
    Mock returning Library object for MOCK_WHITENOISE_SAMPLES_PATH directory
    """
    yield Library(config=mock_empty_config, path=MOCK_WHITENOISE_SAMPLES_PATH)


@pytest.fixture
def oodi_empty_client(mock_empty_config_file) -> Iterator[Oodi]:
    """
    Yield Oodi client with mocked empty config
    """
    yield Oodi()


@pytest.fixture
def oodi_default_client(mock_default_config_file) -> Iterator[Oodi]:
    """
    Yield Oodi client with mocked default config
    """
    yield Oodi()
