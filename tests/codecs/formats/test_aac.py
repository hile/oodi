"""
Unit tests for oodi.codecs.formats.aac module
"""
from pathlib import Path

from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats.aac import Aac

from .validators import validate_codec_properties, TEST_FILENAME_NO_MATCH

TEST_FILENAME_MATCH = f'test case.{CodecFormat.AAC.value}'


def test_codecs_formats_aac_properties(mock_empty_config):
    """
    Test properties of the Aac codec class
    """
    validate_codec_properties(Aac(mock_empty_config), mock_empty_config.__path__)


def test_codecs_formats_aac_match_file_no_match(mock_empty_config, tmpdir):
    """
    Test matching unexpected filename to aac codec
    """
    assert Aac(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_NO_MATCH)) is False


def test_codecs_formats_aac_match_file_matches(mock_empty_config, tmpdir):
    """
    Test matching a mp3 filename to aac codec
    """
    assert Aac(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_MATCH)) is True
