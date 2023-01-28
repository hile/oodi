"""
Unit tests for oodi.codecs.formats.caf module
"""
from pathlib import Path

from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats.caf import Caf

from .validators import validate_codec_properties, TEST_FILENAME_NO_MATCH

TEST_FILENAME_MATCH = f'test case.{CodecFormat.CAF.value}'


def test_codecs_formats_caf_properties(mock_empty_config):
    """
    Test properties of the Caf codec class
    """
    validate_codec_properties(Caf(mock_empty_config), mock_empty_config.__path__)


def test_codecs_formats_caf_match_file_no_match(mock_empty_config, tmpdir):
    """
    Test matching unexpected filename to caf codec
    """
    assert Caf(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_NO_MATCH)) is False


def test_codecs_formats_caf_match_file_matches(mock_empty_config, tmpdir):
    """
    Test matching a caf filename to caf codec
    """
    assert Caf(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_MATCH)) is True
