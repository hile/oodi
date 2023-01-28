"""
Oodi client main class
"""
from typing import Optional

from sys_toolkit.base import LoggingBaseClass

from .configuration import Configuration


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
