"""
Audio file
"""
from typing import Optional, TYPE_CHECKING
from pathlib import Path

from ..codecs.constants import CodecFormat
from ..codecs.formats.base import Codec

if TYPE_CHECKING:
    from ..configuration import Configuration
    from .album import Album
    from .tree import Library


# pylint: disable=too-few-public-methods
class AudioFile:
    """
    Audio file optionally linked to an album and library
    """
    config: 'Configuration'
    library: Optional['Library']
    album: Optional['Album']
    path: Path
    codec: Codec

    def __init__(self,
                 config: 'Configuration',
                 path: Path,
                 library: Optional['Library'] = None,
                 album: Optional['Album'] = None,
                 codec_format: Optional[CodecFormat] = None) -> None:
        self.config = config
        self.path = path.resolve()
        self.library = library
        self.album = album
        self.codec = self.__detect_file_codec__(self.path, codec_format)

    def __detect_file_codec__(self,
                              path: Path,
                              codec_format: Optional[CodecFormat] = None) -> Codec:
        """
        Detect codec for audio file
        """
        if codec_format is not None:
            return self.config.get_codec(codec_format)
        return self.config.codecs.get_codec_for_path(path)

    def __repr__(self):
        return str(self.path)

    def __eq__(self, other):
        return self.path == other.path

    def __ne__(self, other):
        return self.path != other.path

    def __ge__(self, other):
        return self.path >= other.path

    def __gt__(self, other):
        return self.path > other.path

    def __le__(self, other):
        return self.path <= other.path

    def __lt__(self, other):
        return self.path < other.path
