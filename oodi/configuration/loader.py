"""
Load oodi user configuratin file
"""
from pathlib import Path
from typing import Optional, Union

from sys_toolkit.configuration.base import ConfigurationSection
from sys_toolkit.configuration.yaml import YamlConfiguration

from ..codecs.constants import CodecFormat
from ..codecs.formats.base import Codec
from ..codecs.loader import Codecs
from ..exceptions import ConfigurationError


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
        self.codecs = Codecs(self)

    def __get_default_config_path__(self) -> Path:
        """
        Return default configuration file path
        """
        # pylint: disable=import-outside-toplevel
        from ..constants import USER_CONFIG_DIRECTORY, OODI_CONFIG_FILE
        return USER_CONFIG_DIRECTORY.joinpath(OODI_CONFIG_FILE)

    def get_codec(self, value: Optional[Union[str, CodecFormat]] = None) -> Optional[Codec]:
        """
        Get codec by name as string or by CodecFormat enum
        """
        if value is None:
            return None

        if isinstance(value, str):
            try:
                value = CodecFormat(value)
            except ValueError as error:
                raise ConfigurationError(f'Invalid codec format name: {value}') from error

        if not isinstance(value, CodecFormat):
            raise ConfigurationError(f'Unexpected value for get_codec: {type(value)} {value}')

        return self.codecs.get_codec(value)
