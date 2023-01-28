"""
Loader for codes format parsers
"""
from pathlib import Path
from typing import Optional, Union, TYPE_CHECKING

from oodi.library.tree import LibraryItem

from .constants import CodecFormat

if TYPE_CHECKING:
    from oodi.configuration.loader import Configuration


class Codecs:
    """
    Codec loader
    """
    def __init__(self, config: 'Configuration') -> None:
        self.config = config

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
        return None
