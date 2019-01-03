
import os
import tempfile

import ruamel.yaml

from . import CONFIG_PATH

DEFAULT_CONFIG_PATH = os.path.join(CONFIG_PATH, 'config.yaml')

CONFIG_FIELDS = (
    'tmpdir',
)


class ConfigurationError(Exception):
    pass


class ConfigurationSection(dict):
    """
    App module specific configuration section

    Common parent class for codec, library etc configuration sections
    """
    defaults = os.path.join(__file__, 'defaults.yaml')
    default_configuration = {}

    def __init__(self, configuration):
        super().__init__()
        self.configuration = configuration

        if os.path.isfile(self.defaults):
            self.load_configuration_file(self.defaults)

    def load_configuration_file(self, filename):
        """
        Load configuration from yaml file
        """
        try:
            with open(filename, 'r') as fd:
                yaml = ruamel.yaml.YAML()
                data = yaml.load(fd)
                self.update(data)
        except Exception as e:
            raise ConfigurationError('Error loading configuration file {}: {}'.format(filename, e))

    def load(self, data):
        """
        Load raw data
        """
        self.update(data)


class Configuration:
    """
    Configuration file parser
    """

    def __init__(self, path=DEFAULT_CONFIG_PATH):
        """
        Load base configuration for oodi with codecs and libraries

        Also loads given configuration file if available
        """

        from .codecs.configuration import CodecConfiguration
        from .library.configuration import LibraryConfiguration

        self.path = path
        self.__tmp_dir__ = None

        self.codecs = CodecConfiguration(self)
        self.library = LibraryConfiguration(self)

        for field in CONFIG_FIELDS:
            setattr(self, field, None)
        self.load(os.path.join(os.path.dirname(__file__), 'defaults.yaml'))

        if self.path:
            self.load(self.path)

    def __del__(self):
        """
        Try to cleanup created temporary directory when configuration is deleted
        """
        try:
            if self.__tmp_dir__ is not None:
                del self.__tmp_dir__
        except Exception:
            pass

    def get_temporary_file_path(self, suffix=None):
        if self.__tmp_dir__ is None:
            self.__tmp_dir__ = tempfile.TemporaryDirectory(prefix='/tmp/')
        return tempfile.mktemp(
            dir='{}/'.format(self.__tmp_dir__.name),
            suffix=suffix,
        )

    def load(self, path):
        """
        Load specified configuration file

        Also configures self.codecs and self.libraries child classes
        """

        data = {}
        if os.path.isfile(os.path.realpath(path)):
            try:
                with open(path, 'r') as fd:
                    yaml = ruamel.yaml.YAML()
                    data = yaml.load(fd)
            except Exception as e:
                raise ConfigurationError('Error loading configuration file {}: {}'.format(path, e))
        else:
            raise ConfigurationError('Configuration is not a file: {}'.format(path))

        if isinstance(data, dict):
            for field in CONFIG_FIELDS:
                value = data.get(field, None)
                if value is not None:
                    setattr(self, field, value)

            if 'codecs' in data:
                self.codecs.load(data['codecs'])

            if 'library' in data:
                self.library.load(data['library'])
