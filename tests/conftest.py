"""
Pytest unit test configuration for oodi
"""
from pathlib import Path
from shutil import copyfile, copytree, rmtree
from typing import Iterator

import pytest

from oodi.client import Oodi
from oodi.codecs.constants import CodecFormat
from oodi.configuration import Configuration
from oodi.library.album import Album
from oodi.library.tree import Library
from oodi.metadata.constants import ALBUMART_SUPPORTED_FILENAMES, BOOKLET_SUPPORTED_FILENAMES

MOCK_MESSAGE = 'Mock message'

MOCK_DATA = Path(__file__).parent.joinpath('mock')
MOCK_METADATA = MOCK_DATA.joinpath('metadata')
MOCK_CONFIG_DIRECTORY = MOCK_DATA.joinpath('config/default')
MOCK_EMPTY_CONFIG_DIRECTORY = MOCK_DATA.joinpath('config/empty')

# Directory with whitenoise samples
MOCK_WHITENOISE_SAMPLES_PATH = MOCK_DATA.joinpath('samples')
MOCK_WHITENOISE_SAMPLES_FOLDER_COUNT = 3
MOCK_METADATA_FILES_COUNT = 8
MOCK_WHITENOISE_SAMPLES_COUNT = 9

# Mocked album paths that do not exist
TEST_ALBUM_PATHS = (
    Path('Album/In Library'),
)

# List of all sample files as standard Path objects from the test data directory
WHITENOISE_SAMPLE_FILES = [
    item
    for item in list(MOCK_WHITENOISE_SAMPLES_PATH.glob('**/*'))
    if item.is_file()
]

MOCK_METADATA_FILES = [path for path in MOCK_METADATA.glob('**/*') if path.is_file()]
MOCK_ALBUMART_FILES = [
    path
    for path in MOCK_METADATA_FILES
    if path.name in ALBUMART_SUPPORTED_FILENAMES
]
MOCK_BOOKLET_FILES = [
    path
    for path in MOCK_METADATA_FILES
    if path.name in BOOKLET_SUPPORTED_FILENAMES
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


@pytest.fixture(params=MOCK_BOOKLET_FILES)
def mock_booklet_file(request):
    """
    Mock fixture to list all available booklet files in test data
    """
    yield request.param


@pytest.fixture
def mock_empty_library(mock_empty_config, tmpdir) -> Iterator[Library]:
    """
    Mock returning Library object for tmpdir directory
    """
    yield Library(config=mock_empty_config, path=Path(tmpdir.strpath))


@pytest.fixture
def mock_sample_library(mock_empty_config, tmpdir) -> Iterator[Library]:
    """
    Generate a Library object for samples with albumart and bookmark files
    from mock data directory
    """
    albumart = MOCK_ALBUMART_FILES[0]
    booklet = MOCK_BOOKLET_FILES[0]
    path = Path(tmpdir.strpath, 'music')

    copytree(MOCK_WHITENOISE_SAMPLES_PATH, path)
    copyfile(albumart, path.joinpath(albumart.name))
    copyfile(booklet, path.joinpath(booklet.name))
    for item in path.glob('**/*'):
        if item.is_dir():
            copyfile(albumart, item.joinpath(albumart.name))
            copyfile(booklet, item.joinpath(booklet.name))

    yield Library(
        config=mock_empty_config,
        path=path,
        formats=[codec_format.value for codec_format in CodecFormat]
    )


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
