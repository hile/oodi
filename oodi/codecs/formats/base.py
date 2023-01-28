"""
Common base class for Codec classes
"""
from pathlib import Path
from typing import Tuple, TYPE_CHECKING

from ..constants import CodecFormat

if TYPE_CHECKING:
    from oodi.configuration.loader import Configuration


class Codec:
    """
    Common base class for codecs
    """
    codec_format: CodecFormat
    description: str
    default_suffix: str
    suffixes: Tuple[str] = ()
    mimetypes: Tuple[str] = ()

    def __init__(self, config: 'Configuration') -> None:
        self.config = config

    def __repr__(self) -> str:
        return f'{self.codec_format.value} {self.description}'

    # pylint: disable=unused-argument
    def match_file_properties(self, path: Path) -> bool:
        """
        Internal class specific function to check if file properties match
        this codec.

        By default this returns always True. Override the method in child
        class when more detailed check methods are required
        """
        return True

    def match_file(self, path: Path) -> bool:
        """
        Check if specified file matches this codec
        """
        if not path.suffix.lstrip('.') in self.suffixes:
            return False
        return self.match_file_properties(path)
