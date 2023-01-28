"""
Oodi loader for folders of music files as music libraries
"""
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

from pathlib_tree.tree import Tree, TreeItem

if TYPE_CHECKING:
    from oodi.configuration.loader import Configuration


class LibraryItem(TreeItem):
    """
    File in audio library
    """
    config: 'Configuration'

    # pylint: disable=unused-argument
    def __init__(self, path: Path, config: Optional['Configuration'] = None) -> None:
        self.config = config
        TreeItem.__init__(self)


class Library(Tree):
    """
    Oodi audio file library linked to oodi configuration
    """
    __file_loader_class__ = LibraryItem

    config: 'Configuration'
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
                 filesystem_encoding: Optional[str] = None,
                 default_format: Optional[str] = None,
                 formats: Optional[List[str]] = None,
                 label: Optional[str] = None,
                 description: Optional[str] = None) -> None:

        self.config = config
        self.default_format = default_format
        self.formats = list(formats) if formats else []
        self.filesystem_encoding = filesystem_encoding
        self.label = label if label else ''
        self.description = description if description else ''
        self.excluded = list(excluded) if isinstance(excluded, (tuple, list)) else []

        super().__init__(
            path=path,
            create_missing=create_missing,
            sorted=sorted,
            mode=mode,
            excluded=excluded
        )
