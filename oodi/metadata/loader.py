"""
Metadata loading
"""
from pathlib import Path
from typing import Any, List, Union, TYPE_CHECKING

from .constants import (
    ALBUMART_SUPPORTED_FILENAMES,
    BOOKLET_SUPPORTED_FILENAMES,
)
from ..exceptions import MetadataError
from .formats.albumart import AlbumArt
from .formats.booklet import Booklet

if TYPE_CHECKING:
    from ..configuration import Configuration
    from ..library.album import Album
    from ..library.tree import LibraryItem


class AlbumMetadata:
    """
    Metadata loader for album objects
    """
    album: 'Album'
    albumart: List[AlbumArt]
    booklets: List[Booklet]

    def __init__(self, album: 'Album') -> None:
        self.album = album
        self.albumart = []
        self.booklets = []

    @property
    def config(self) -> 'Configuration':
        """
        Return configuration via the Album's library object
        """
        return self.album.library.config

    def debug(self, *args: List[Any]) -> None:
        """
        Send debug message to stderr if debug mode is enabled
        """
        self.album.debug(*args)

    def error(self, *args: List[Any]) -> None:
        """
        Send error message to stderr
        """
        self.album.error(*args)

    def message(self, *args: List[Any]) -> None:
        """
        Show message to stdout unless silent flag is set
        """
        self.album.message(*args)

    def add_metadata_file(self, metadata_file: Union['LibraryItem', Path]) -> 'LibraryItem':
        """
        Add a metadata file to the album
        """
        kwargs = {
            'config': self.config,
            'library': self.album.library,
            'album': self.album,
            'path': metadata_file,
        }
        if metadata_file.name in ALBUMART_SUPPORTED_FILENAMES:
            albumart = AlbumArt(**kwargs)
            self.albumart.append(albumart)
            return albumart
        if metadata_file.name in BOOKLET_SUPPORTED_FILENAMES:
            booklet = Booklet(**kwargs)
            self.booklets.append(booklet)
            return booklet
        raise MetadataError(f'Unknown file type: {metadata_file}')
