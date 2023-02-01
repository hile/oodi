"""
Albums in music library
"""
from pathlib import Path
from typing import Any, List, Optional, Union, TYPE_CHECKING

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
        return str(self.relative_path)

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
