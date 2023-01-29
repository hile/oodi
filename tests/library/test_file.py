"""
Unit tests for oodi.library.file module
"""
from pathlib import Path

from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats.base import Codec
from oodi.configuration import Configuration
from oodi.library.file import AudioFile

MOCK_FILENAME = ''


def validate_audiofile_properties(config: Configuration, obj: AudioFile) -> None:
    """
    Validate some common properties of an audiofile object
    """
    assert isinstance(config, Configuration)
    assert isinstance(obj.codec, Codec)
    assert isinstance(obj.__repr__(), str)
    assert obj.library is None


def test_audio_file_properties(mock_empty_config, mock_sample_file) -> None:
    """
    Test loading the sample audio files from test data as Audiofile objects
    that are not linked to any library
    """
    obj = AudioFile(mock_empty_config, mock_sample_file)
    assert obj.path.is_file()
    validate_audiofile_properties(mock_empty_config, obj)


def test_audio_file_missing_file(mock_empty_config, tmpdir) -> None:
    """
    Test initializing AudioFile object for a non-existing file that does not
    belong to any library
    """
    path = Path(tmpdir.strpath, MOCK_FILENAME)
    obj = AudioFile(mock_empty_config, path=path, codec_format=CodecFormat.ALAC)
    assert not obj.path.is_file()
    validate_audiofile_properties(mock_empty_config, obj)
