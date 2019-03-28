
import os
import unittest

from uuid import uuid4

TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), 'files')


class ConfigurationTests(unittest.TestCase):
    """
    Tests loading of oodi configuration
    """

    def check_configuration_objects(self, config):
        """
        Check basic object types in loaded configuration
        """
        from oodi.configuration import Configuration
        from oodi.codecs.configuration import CodecConfiguration
        from oodi.library.configuration import LibraryConfiguration

        # Check we get correct objects
        self.assertIsInstance(config, Configuration)
        self.assertIsInstance(config.codecs, CodecConfiguration)
        self.assertIsInstance(config.library, LibraryConfiguration)

        # Check sections were loaded for codecs from defaults.yaml
        for section in ('encoders', 'decoders', 'testers'):
            self.assertTrue(section in config.codecs, 'Missing codec configuration section {}'.format(section))
            section = config.codecs[section]

    def test_configuration_default_configuration(self):
        """
        Test loading configuration with no options
        """
        from oodi.configuration import Configuration
        config = Configuration()
        self.check_configuration_objects(config)

    def test_configuration_no_path(self):
        """
        Test configuration can be loaded by passing None as path
        """
        from oodi.configuration import Configuration
        config = Configuration(path=None)
        self.check_configuration_objects(config)

    def test_configuration_load_empty_configuration(self):
        """
        Test loading empty yaml configuration
        """
        from oodi.configuration import Configuration
        config = Configuration(os.path.join(TEST_FILES_PATH, 'empty.yaml'))
        self.check_configuration_objects(config)

    def test_configuration_load_invalid_configuration(self):
        """
        Test loading invalid yaml configuration.

        The test file is actually .ini file
        """
        from oodi.configuration import Configuration, ConfigurationError
        with self.assertRaises(ConfigurationError):
            Configuration(os.path.join(TEST_FILES_PATH, 'invalid.yaml'))

    def test_configuration_load_custom_codec_configuration(self):
        """
        Test loading custom settings to codecs configuration

        Overrides some attributes, check here these are loaded to configuration
        """
        from oodi.configuration import Configuration

        config = Configuration(os.path.join(TEST_FILES_PATH, 'codecs.yaml'))
        self.check_configuration_objects(config)

        self.assertEqual(config.codecs.get('aac').get('bitrate'), 123456)
        self.assertEqual(config.codecs.get('encoders').get('wav'), [])

    def test_configuration_load_directory_path(self):
        """
        Test loading directory path as yaml configuration
        """
        from oodi.configuration import Configuration, ConfigurationError
        with self.assertRaises(ConfigurationError):
            Configuration(path='/')

    def test_configuration_invalid_file_path(self):
        """
        Test loading invalid path as yaml configuration
        """
        from oodi.configuration import Configuration, ConfigurationError
        with self.assertRaises(ConfigurationError):
            Configuration(os.path.join('/{}'.format(uuid4())))
