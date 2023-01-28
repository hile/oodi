"""
Pytest unit test configuration for oodi
"""
from pathlib import Path
from shutil import rmtree
from typing import Iterator

import pytest

from oodi.configuration import Configuration

MOCK_DATA = Path(__file__).parent.joinpath('mock')
MOCK_CONFIG_DIRECTORY = MOCK_DATA.joinpath('config/default')
MOCK_EMPTY_CONFIG_DIRECTORY = MOCK_DATA.joinpath('config/empty')


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
