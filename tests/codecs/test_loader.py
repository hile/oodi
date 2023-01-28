"""
Unit tests for oodi.codecs.loader module
"""

from pathlib import Path
from oodi.codecs.loader import Codecs


def test_codecs_loader_properties(mock_empty_config) -> None:
    """
    Test properties of codecs loader with empty configuration
    """
    assert isinstance(mock_empty_config.codecs, Codecs)
    assert mock_empty_config.codecs.config == mock_empty_config


def test_codecs_loader_get_codec_for_path_directory(mock_empty_config, tmpdir) -> None:
    """
    Test looking up codec for a directory. This method always returns
    None even when there is a matching extension
    """
    path = Path(tmpdir.strpath, 'empty-directory.wav')
    path.mkdir()
    assert mock_empty_config.codecs.get_codec_for_path(path) is None


def test_codecs_loader_get_codec_for_path_without_extension(mock_empty_config, tmpdir) -> None:
    """
    Test looking up codec for a file missing file path without extension
    """
    path = Path(tmpdir.strpath, 'empty-directory.wav')
    assert not path.exists()
    assert mock_empty_config.codecs.get_codec_for_path(path) is None
