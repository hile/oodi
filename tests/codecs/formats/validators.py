"""
Validators for common codec class properties
"""
from pathlib import Path

from oodi.codecs.formats.base import Codec

TEST_FILENAME_NO_MATCH = 'test file with no codec match.invalid'


def validate_codec_properties(codec: Codec, invalid_path: Path) -> None:
    """
    Validate some common codec properties
    """
    assert isinstance(codec.__repr__(), str)
    assert isinstance(codec, Codec)
    assert codec.match_file_properties(invalid_path) is True
    assert codec.match_file(invalid_path) is False
