"""
Unit tests for oodi.codecs.formats.opus module
"""
from pathlib import Path

from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats.opus import Opus

from .validators import validate_codec_properties, TEST_FILENAME_NO_MATCH

TEST_FILENAME_MATCH = f'test case.{CodecFormat.OPUS.value}'


def test_codecs_formats_opus_properties(mock_empty_config):
    """
    Test properties of the opus codec class
    """
    validate_codec_properties(Opus(mock_empty_config), mock_empty_config.__path__)


def test_codecs_formats_opus_match_file_no_match(mock_empty_config, tmpdir):
    """
    Test matching unexpected filename to opus codec
    """
    assert Opus(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_NO_MATCH)) is False


def test_codecs_formats_opus_match_file_matches(mock_empty_config, tmpdir):
    """
    Test matching a opus filename to opus codec
    """
    assert Opus(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_MATCH)) is True
