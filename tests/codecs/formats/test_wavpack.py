"""
Unit tests for oodi.codecs.formats.wavpack module
"""
from pathlib import Path

from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats.wavpack import Wavpack

from .validators import validate_codec_properties, TEST_FILENAME_NO_MATCH

TEST_FILENAME_MATCH = f'test case.{CodecFormat.WAVPACK.value}'


def test_codecs_formats_wavpack_properties(mock_empty_config):
    """
    Test properties of the wavpack codec class
    """
    validate_codec_properties(Wavpack(mock_empty_config), mock_empty_config.__path__)


def test_codecs_formats_wavpack_match_file_no_match(mock_empty_config, tmpdir):
    """
    Test matching unexpected filename to wavpack codec
    """
    assert Wavpack(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_NO_MATCH)) is False


def test_codecs_formats_wavpack_match_file_matches(mock_empty_config, tmpdir):
    """
    Test matching a wavpack filename to wavpack codec
    """
    assert Wavpack(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_MATCH)) is True
