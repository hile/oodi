"""
Unit tests for oodi.codecs.loader module
"""
from pathlib import Path
from oodi.codecs.formats.base import Codec
from oodi.codecs.loader import Codecs


def test_codecs_loader_properties(mock_empty_config) -> None:
    """
    Test properties of codecs loader with empty configuration
    """
    assert isinstance(mock_empty_config.codecs, Codecs)
    assert mock_empty_config.codecs.config == mock_empty_config


def test_codecs_loader_get_codec_format(mock_empty_config, mock_codec_format) -> None:
    """
    Test looking up a codec with all valid path from all codec formats
    """
    codec = mock_empty_config.codecs.get_codec(mock_codec_format)
    assert isinstance(codec, Codec)


def test_codecs_loader_get_codec_for_mimetype_invalid(mock_empty_config) -> None:
    """
    Test looking up codec for unexpected MIME type
    """
    assert mock_empty_config.codecs.get_codec_for_mimetype('text/plain') is None


def test_codecs_loader_get_codec_for_mimetype_valid(mock_empty_config, mock_codec_mimetype) -> None:
    """
    Test looking up a codec with all valid MIME types from all codecs
    """
    codec = mock_empty_config.codecs.get_codec_for_mimetype(mock_codec_mimetype)
    assert isinstance(codec, Codec)


def test_codecs_loader_get_codec_for_path_without_extension(mock_empty_config, tmpdir) -> None:
    """
    Test looking up codec for a file missing file path without extension
    """
    path = Path(tmpdir.strpath, 'empty-directory.wav')
    assert not path.exists()
    assert mock_empty_config.codecs.get_codec_for_path(path) is None


def test_codecs_loader_get_codec_for_path_directory(mock_empty_config, tmpdir) -> None:
    """
    Test looking up codec for a directory. This method always returns
    None even when there is a matching extension
    """
    path = Path(tmpdir.strpath, 'empty-directory.wav')
    path.mkdir()
    assert mock_empty_config.codecs.get_codec_for_path(path) is None


def test_codecs_loader_get_codec_for_path_invalid_file(mock_empty_config) -> None:
    """
    Test looking up codec for unexpected filename
    """
    assert mock_empty_config.codecs.get_codec_for_path(Path(__file__)) is None


def test_codecs_loader_get_codec_for_path_valid(mock_empty_config, mock_codec_filename) -> None:
    """
    Test looking up a codec with all valid path from all codecs
    """
    codec = mock_empty_config.codecs.get_codec_for_path(mock_codec_filename)
    assert isinstance(codec, Codec)
