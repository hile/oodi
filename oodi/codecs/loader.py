"""
Loader for codes format parsers
"""
from pathlib import Path
from typing import List, Optional, Union, TYPE_CHECKING

from oodi.library.tree import LibraryItem

from .constants import CodecFormat
from .formats import CODECS
from .formats.base import Codec

if TYPE_CHECKING:
    from oodi.configuration.loader import Configuration


class Codecs:
    """
    Codec loader
    """
    __codecs__: List[Codec]
    __suffix_map__: dict
    __mimetype_map__: dict

    def __init__(self, config: 'Configuration') -> None:
        self.config = config
        self.__initialize_codecs__()

    def __initialize_codec_suffix_map__(self, codec: Codec) -> None:
        """
        Initialize suffix map items for codec
        """
        for suffix in codec.suffixes:
            if suffix not in self.__suffix_map__:
                self.__suffix_map__[suffix] = []
            self.__suffix_map__[suffix].append(codec)

    def __initialize_codec_mimetype_map__(self, codec: Codec) -> None:
        """
        Initialize MIME type map items for codec
        """
        for mimetype in codec.mimetypes:
            if mimetype in self.__mimetype_map__:
                raise ValueError(f'duplicate codec MIME type {mimetype}')
            self.__mimetype_map__[mimetype] = codec

    def __initialize_codecs__(self) -> NotImplementedError:
        """
        Return codec objects linked to configuration
        """
        self.__codecs__ = []
        self.__suffix_map__ = {}
        self.__mimetype_map__ = {}
        for loader in CODECS:
            codec = loader(self)
            self.__codecs__.append(codec)
            self.__initialize_codec_suffix_map__(codec)
            self.__initialize_codec_mimetype_map__(codec)

    def get_codec_for_mimetype(self, mimetype: str) -> Optional[CodecFormat]:
        """
        Get code for specified MIME type

        Params:
        str: MIME type string

        Returns:
        Codec matching the path or None
        """
        return self.__mimetype_map__.get(mimetype, None)

    def get_codec_for_path(self, path: Union[LibraryItem, Path]) -> Optional[CodecFormat]:
        """
        Get codec for specified path

        Params:
        path: Library item or Path object

        Returns:
        Codec matching the path or None
        """
        if path.is_dir() or not path.suffix:
            return None
        codecs = self.__suffix_map__.get(path.suffix.lstrip('.'), None)
        if codecs is None:
            return None
        for codec in codecs:
            if codec.match_file(path):
                return codec
        return None
