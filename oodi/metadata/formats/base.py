"""
Oodi audio file metadata common base class
"""
from typing import Optional, TYPE_CHECKING

from pathlib import Path

if TYPE_CHECKING:
    from ...configuration import Configuration
    from ...library.album import Album
    from ...library.tree import Library


class Metadata:
    """
    Base class for audio library metadata files
    """
    config: 'Configuration'
    library: Optional['Library']
    album: Optional['Album']
    path: Path

    def __init__(self,
                 config: 'Configuration',
                 path: Path,
                 library: Optional['Library'] = None,
                 album: Optional['Album'] = None) -> None:
        self.config = config
        self.path = path.resolve()
        self.library = library
        self.album = album

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
