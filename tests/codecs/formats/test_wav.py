"""
Unit tests for oodi.codecs.formats.wav module
"""
from pathlib import Path

from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats.wav import Wav

from .validators import validate_codec_properties, TEST_FILENAME_NO_MATCH

TEST_FILENAME_MATCH = f'test case.{CodecFormat.WAV.value}'


def test_codecs_formats_wav_properties(mock_empty_config):
    """
    Test properties of the Wav codec class
    """
    validate_codec_properties(Wav(mock_empty_config), mock_empty_config.__path__)


def test_codecs_formats_wav_match_file_no_match(mock_empty_config, tmpdir):
    """
    Test matching unexpected filename to wav codec
    """
    assert Wav(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_NO_MATCH)) is False


def test_codecs_formats_wav_match_file_matches(mock_empty_config, tmpdir):
    """
    Test matching a wav filename to wav codec
    """
    assert Wav(mock_empty_config).match_file(Path(tmpdir.strpath, TEST_FILENAME_MATCH)) is True
