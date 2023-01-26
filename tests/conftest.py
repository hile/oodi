"""
Pytest unit test configuration for oodi
"""
from pathlib import Path
from shutil import rmtree
import pytest

MOCK_DATA = Path(__file__).parent.joinpath('mock')
MOCK_CONFIG_DIRECTORY = MOCK_DATA.joinpath('config/default')
MOCK_EMPTY_CONFIG_DIRECTORY = MOCK_DATA.joinpath('config/empty')


@pytest.fixture
def mock_missing_config(monkeypatch, tmpdir):
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
def mock_empty_config(monkeypatch):
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
def mock_default_config(monkeypatch):
    """
    Mock constant oodi.constants.USER_CONFIG_DIRECTORY to return
    mocked directory tests/mock/config/default
    """
    monkeypatch.setattr(
        'oodi.constants.USER_CONFIG_DIRECTORY',
        MOCK_CONFIG_DIRECTORY,
    )
    yield MOCK_CONFIG_DIRECTORY
