"""
Unit tests for oodi.codecs.formats.vorbis module
"""
from pathlib import Path

from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats.vorbis import Vorbis

from .validators import validate_codec_properties, TEST_FILENAME_NO_MATCH

TEST_FILENAME_MATCH = f'test case.{CodecFormat.VORBIS.value}'


def test_codecs_formats_vorbis_properties(mock_empty_config):
    """
    Test properties of the Vorbis codec class
    """
    validate_codec_properties(Vorbis(mock_empty_config), mock_empty_config.__path__)


def test_codecs_formats_vorbis_match_file_no_match(mock_empty_config, tmpdir):
    """
    Test matching unexpected filename to vorbis codec
    """
    assert Vorbis(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_NO_MATCH)) is False


def test_codecs_formats_vorbis_match_file_matches(mock_empty_config, tmpdir):
    """
    Test matching a vorbis filename to vorbis codec
    """
    assert Vorbis(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_MATCH)) is True
