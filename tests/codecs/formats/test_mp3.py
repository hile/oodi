"""
Unit tests for oodi.codecs.formats.mp3 module
"""
from pathlib import Path

from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats.mp3 import Mp3

from .validators import validate_codec_properties, TEST_FILENAME_NO_MATCH

TEST_FILENAME_MATCH = f'test case.{CodecFormat.MP3.value}'


def test_codecs_formats_mp3_properties(mock_empty_config):
    """
    Test properties of the Mp3 codec class
    """
    validate_codec_properties(Mp3(mock_empty_config), mock_empty_config.__path__)


def test_codecs_formats_mp3_match_file_no_match(mock_empty_config, tmpdir):
    """
    Test matching unexpected filename to mp3 codec
    """
    assert Mp3(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_NO_MATCH)) is False


def test_codecs_formats_mp3_match_file_matches(mock_empty_config, tmpdir):
    """
    Test matching a mp3 filename to mp3 codec
    """
    assert Mp3(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_MATCH)) is True
