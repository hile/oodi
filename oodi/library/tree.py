"""
Oodi loader for folders of music files as music libraries
"""
import itertools

from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

from pathlib_tree.tree import Tree, TreeItem

from ..exceptions import ConfigurationError
from ..codecs.constants import DEFAULT_AUDIO_CODEC_FORMAT
from ..codecs.formats.base import Codec

if TYPE_CHECKING:
    from ..configuration.loader import Configuration


class LibraryItem(TreeItem):
    """
    File in audio library
    """
    config: 'Configuration'

    # pylint: disable=unused-argument
    def __init__(self, path: Path, config: Optional['Configuration'] = None) -> None:
        self.config = config
        TreeItem.__init__(self)


# pylint: disable=too-few-public-methods
class LibraryCodecs:
    """
    Link
    Container to list codecs linked to a Library object based on the formats specified
    for the library
    """
    library: 'Library'
    default: Optional[Codec]
    formats: List[Codec]

    def __init__(self,
                 library: 'Library',
                 default: Optional[str] = None,
                 formats: Optional[List[str]] = None) -> None:

        default = default if default is not None else DEFAULT_AUDIO_CODEC_FORMAT
        if formats is None:
            formats = [default]

        self.library = library
        self.default = library.config.get_codec(default)
        self.formats = [library.config.get_codec(value) for value in formats]

        if self.default not in self.formats:
            raise ConfigurationError(
                f'Library configuration error: default codec {self.default} '
                'is not in included in configured formats'
            )

    @property
    def suffixes(self) -> List[str]:
        """
        Return suffixes for all configured codecs configured to self.formats

        Values are ensured to contain a . in the beginning to match Path.suffix lookups
        """
        return [
            f""".{suffix.lstrip('.')}"""
            for suffix in sorted(set(itertools.chain(*[codec.suffixes for codec in self.formats])))
        ]


class Library(Tree):
    """
    Oodi audio file library linked to oodi configuration
    """
    __file_loader_class__ = LibraryItem

    config: 'Configuration'
    codecs = LibraryCodecs
    label: str
    description: str
    default_format: str
    filesystem_encoding: str
    formats: List[str]
    excluded: List[str]
    sorted: bool
    mode: int

    # pylint: disable=redefined-builtin
    # pylint: disable=arguments-differ
    # pylint: disable=unused-argument
    def __new__(cls,
                path: Path,
                create_missing: bool = False,
                sorted: bool = True,
                excluded: Optional[List[str]] = None,
                mode: Optional[int] = None,
                config: Optional['Configuration'] = None,
                library: Optional['Library'] = None,
                filesystem_encoding: Optional[str] = None,
                default_format: Optional[str] = None,
                formats: Optional[List[str]] = None,
                description: Optional[str] = None) -> None:
        path = Path(path).expanduser()
        if create_missing and not path.exists():
            path.mkdir(parents=True)
        return super().__new__(cls, path, excluded=excluded)

    def __init__(self,
                 path: Path,
                 create_missing: bool = False,
                 sorted: bool = True,
                 mode: Optional[int] = None,
                 excluded: Optional[List[str]] = None,
                 config: Optional['Configuration'] = None,
                 library: Optional['Library'] = None,
                 filesystem_encoding: Optional[str] = None,
                 default_format: Optional[str] = None,
                 formats: Optional[List[str]] = None,
                 label: Optional[str] = None,
                 description: Optional[str] = None) -> None:

        self.library = library if library is not None else self
        self.config = config
        self.codecs = LibraryCodecs(self, default=default_format, formats=formats)

        self.label = label if label else ''
        self.description = description if description else ''
        self.excluded = list(excluded) if isinstance(excluded, (tuple, list)) else []
        self.filesystem_encoding = filesystem_encoding

        super().__init__(
            path=path,
            create_missing=create_missing,
            sorted=sorted,
            mode=mode,
            excluded=excluded
        )

    def __load_tree__(self, item) -> 'Library':
        """
        Load sub directory as Library linked to this item
        """
        return self.__class__(
            item,
            sorted=self.sorted,
            excluded=self.excluded,
            config=self.config,
            library=self.library,
        )
