"""
Load oodi user configuratin file
"""
from pathlib import Path
from typing import List, Optional

from sys_toolkit.configuration.base import ConfigurationSection
from sys_toolkit.configuration.yaml import YamlConfiguration

from ..library.tree import Library
from ..constants import (
    DEFAULT_FILESYSTEM_ENCODING,
)


OODI_CONFIG_FILE = 'oodi.yml'


class Configuration(YamlConfiguration):
    """
    Oodi main configuration YAML file
    """
    def __init__(self,
                 path: Path = None,
                 parent: Optional[ConfigurationSection] = None,
                 debug_enabled: bool = False,
                 silent: bool = False) -> None:
        path = path if path is not None else self.__get_default_config_path__()
        super().__init__(path=path, parent=parent, debug_enabled=debug_enabled, silent=silent)

    def __get_default_config_path__(self) -> Path:
        """
        Return default configuration file path
        """
        from ..constants import USER_CONFIG_DIRECTORY  # pylint: disable=import-outside-toplevel
        return USER_CONFIG_DIRECTORY.joinpath(OODI_CONFIG_FILE)

    def get_library(self,
                    path: str,
                    create_missing: bool = False,
                    sorted: bool = True,  # pylint: disable=redefined-builtin
                    excluded: Optional[List[str]] = None,
                    filesystem_encoding: str = DEFAULT_FILESYSTEM_ENCODING,
                    default_format: Optional[str] = None,
                    formats: Optional[List[str]] = None,
                    description: Optional[str] = None) -> Library:
        """
        Return Library object for specified path and settings
        """
        return Library(
            config=self,
            path=path,
            create_missing=create_missing,
            sorted=sorted,
            excluded=excluded,
            filesystem_encoding=filesystem_encoding,
            default_format=default_format,
            formats=formats,
            description=description
        )
