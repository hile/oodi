"""
Load oodi user configuratin file
"""
from pathlib import Path
from typing import Optional

from sys_toolkit.configuration.base import ConfigurationSection
from sys_toolkit.configuration.yaml import YamlConfiguration


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
