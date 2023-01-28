"""
Oodi client main class
"""
from typing import List, Optional

from sys_toolkit.base import LoggingBaseClass

from .configuration import Configuration
from .constants import DEFAULT_FILESYSTEM_ENCODING
from .library.tree import Library


class Oodi(LoggingBaseClass):
    """
    Main class for Oodi client
    """
    def __init__(self,
                 configuration_file: Optional[str] = None,
                 debug_enabled: bool = False,
                 silent: bool = False,
                 logger: Optional[str] = None):
        super().__init__(debug_enabled=debug_enabled, silent=silent, logger=logger)
        self.config = Configuration(
            path=configuration_file,
            debug_enabled=self.__debug_enabled__,
            silent=self.__silent__
        )

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
            config=self.config,
            path=path,
            create_missing=create_missing,
            sorted=sorted,
            excluded=excluded,
            filesystem_encoding=filesystem_encoding,
            default_format=default_format,
            formats=formats,
            description=description
        )
