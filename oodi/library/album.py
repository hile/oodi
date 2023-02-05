"""
Albums in music library
"""
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Iterator, List, Optional, Union, TYPE_CHECKING

from .file import AudioFile

if TYPE_CHECKING:
    from ..codecs.constants import CodecFormat
    from .tree import Library, LibraryItem


class Album:
    """
    Album with audio files in music library
    """
    def __init__(self, library: 'Library', relative_path: Path) -> None:
        self.library = library
        self.relative_path = relative_path
        self.audio_files = []
        self.metadata = []

    def __repr__(self) -> str:
        return str(self.path.resolve())

    @property
    def path(self) -> Path:
        """
        Return full filesystem path to the library album
        """
        return Path(self.library).joinpath(self.relative_path)

    def debug(self, *args: List[Any]) -> None:
        """
        Send debug message to stderr if debug mode is enabled
        """
        self.library.debug(*args)

    def error(self, *args: List[Any]) -> None:
        """
        Send error message to stderr
        """
        self.library.error(*args)

    def message(self, *args: List[Any]) -> None:
        """
        Show message to stdout unless silent flag is set
        """
        self.library.message(*args)

    def add_audio_file(self,
                       audio_file: Union['LibraryItem', Path],
                       codec_format: Optional['CodecFormat'] = None) -> AudioFile:
        """
        Add library item or path to the album
        """
        audio_file = AudioFile(
            config=self.library.config,
            library=self.library,
            album=self,
            path=audio_file,
            codec_format=codec_format
        )
        if audio_file not in self.audio_files:
            self.audio_files.append(audio_file)
        return audio_file

    def add_metadata_file(self, metadata_file: Union['LibraryItem', Path]) -> 'LibraryItem':
        """
        Add a metadata file to the album
        """
        self.metadata.append(metadata_file)


class AlbumPathLookup(MutableMapping):
    """
    Album lookup for albums in a library
    """
    def __init__(self, library: 'Library') -> None:
        super().__init__()
        self.library = library
        self.__items__ = {}

    def __delitem__(self, index: str) -> None:
        """
        Delete specified item from cache
        """
        self.__items__.__delitem__(index)

    def __setitem__(self, index: str, value: Album) -> None:
        """
        Set specified value to given index
        """
        self.__items__.__setitem__(index, value)

    def __getitem__(self, index: str) -> Album:
        """
        Get specified item from cache
        """
        return self.__items__.__getitem__(index)

    def __len__(self) -> int:
        """
        Return size of collection
        """
        return len(self.__items__)

    def __iter__(self) -> Iterator[Album]:
        """
        Set specified value to given index
        """
        return self.__items__.__iter__()

    def debug(self, *args: List[Any]) -> None:
        """
        Send debug message to stderr if debug mode is enabled
        """
        self.library.debug(*args)

    def error(self, *args: List[Any]) -> None:
        """
        Send error message to stderr
        """
        self.library.error(*args)

    def message(self, *args: List[Any]) -> None:
        """
        Show message to stdout unless silent flag is set
        """
        self.library.message(*args)

    def get_album_for_file(self, item: 'LibraryItem') -> Album:
        """
        Return album for the folder of the specified audio file
        """
        album_relative_path = str(Path(item.relative_to(self.library).parent))
        try:
            album = self[album_relative_path]
        except KeyError:
            album = Album(self.library, album_relative_path)
            self[album_relative_path] = album
        return album
