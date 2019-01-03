
import os
import shutil
import unittest

TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), 'files')

TEST_PREFIX_PATHS = ['/tmp/test-prefix-1', '/tmp/test-prefix-2']
TEST_LIBRARY_FORMATS = ['aac', 'mp3']

NEW_LIBRARY_PATH = '/tmp/testlibrary'
NEW_LIBRARY_FORMATS = ['vorbis']
NEW_LIBRARY_EXTENSIONS = ['ogg', 'vorbis']


class LibraryConfigurationTests(unittest.TestCase):
    """
    Tests loading of oodi configuration
    """

    def test_default_configuration(self):
        """
        Test default library configuration
        """

        from oodi.configuration import Configuration
        from oodi.library import Libraries

        config = Configuration()
        self.assertIsInstance(config.library['trees'], list)

        libraries = Libraries(config)
        self.assertIsInstance(libraries.trees, list)

    def test_temporary_directory_cleanup(self):
        """
        Make sure temporary directory is cleared after configuration is
        deleted after garbage collection
        """
        import gc
        from oodi.configuration import Configuration

        configuration = Configuration()
        self.assertIsNone(configuration.__tmp_dir__)

        configuration.get_temporary_file_path('foo')
        tmp_dir = configuration.__tmp_dir__.name
        self.assertTrue(os.path.isdir(tmp_dir))

        del (configuration)
        gc.collect()
        self.assertFalse(os.path.isdir(tmp_dir))

    def test_invalid_configured_formats(self):
        """
        Test configuration where tree has invalid codec name in formats

        Must raise LibraryError when attepting to validate files in tree
        """
        from oodi.configuration import Configuration
        from oodi.library import Libraries
        from oodi.library.exceptions import LibraryError
        from oodi.library.tree import Tree

        config = Configuration(os.path.join(TEST_FILES_PATH, 'invalid_formats.yaml'))
        self.assertIsInstance(config.library['trees'], list)

        libraries = Libraries(config)
        self.assertIsInstance(libraries.trees, list)
        self.assertEqual(len(libraries.trees), 1)
        tree = libraries.trees[0]
        self.assertIsInstance(tree, Tree)
        # Library loaded with invalid codec name, validated during loading of extensions
        with self.assertRaises(LibraryError):
            tree.__load_valid_extensions__()

        libraries = Libraries(config)
        self.assertIsInstance(libraries.trees, list)
        self.assertEqual(len(libraries.trees), 1)
        tree = libraries.trees[0]
        self.assertIsInstance(tree, Tree)
        # Library loaded with invalid codec name, validated also here without explicit
        # call to __load_valid_extensions__
        with self.assertRaises(LibraryError):
            tree.__validate_extension__('test.m4a')

    def test_custom_tree_path(self):
        """
        Test configuration that has custom tree with path
        """

        from oodi.configuration import Configuration
        from oodi.library import Libraries
        from oodi.library.tree import Tree

        if os.path.isdir(NEW_LIBRARY_PATH):
            shutil.rmtree(NEW_LIBRARY_PATH)

        config = Configuration(os.path.join(TEST_FILES_PATH, 'new_library.yaml'))
        self.assertIsInstance(config.library['trees'], list)

        libraries = Libraries(config)
        self.assertIsInstance(libraries.trees, list)
        self.assertEqual(len(libraries.trees), 1)

        tree = libraries.trees[0]
        self.assertIsInstance(tree, Tree)
        self.assertEqual(tree.formats, NEW_LIBRARY_FORMATS)
        self.assertEqual(tree.path, NEW_LIBRARY_PATH)
        self.assertFalse(tree.exists)

        tree.__load_valid_extensions__()
        self.assertEqual(tree.__extensions__, NEW_LIBRARY_EXTENSIONS)
        for extension in NEW_LIBRARY_EXTENSIONS:
            self.assertTrue(tree.__validate_extension__('test.{}'.format(extension)))

        os.makedirs(NEW_LIBRARY_PATH)
        self.assertTrue(tree.exists)
        shutil.rmtree(NEW_LIBRARY_PATH)

    def test_custom_tree_prefixes(self):
        """
        Test library configuration with tree prefixes
        """
        from oodi.configuration import Configuration
        from oodi.library import Libraries
        from oodi.library.tree import Tree

        for path in TEST_PREFIX_PATHS:
            if os.path.isdir(path):
                shutil.rmtree(path)

        config = Configuration(os.path.join(TEST_FILES_PATH, 'library_prefixes.yaml'))
        self.assertIsInstance(config.library['trees'], list)

        libraries = Libraries(config)
        self.assertIsInstance(libraries.trees, list)
        self.assertEqual(len(libraries.trees), 0)

        for path in TEST_PREFIX_PATHS:
            os.makedirs(path)

        config = Configuration(os.path.join(TEST_FILES_PATH, 'library_prefixes.yaml'))
        self.assertIsInstance(config.library['trees'], list)

        libraries = Libraries(config)
        self.assertIsInstance(libraries.trees, list)
        self.assertEqual(len(libraries.trees), len(TEST_PREFIX_PATHS))
        for tree in libraries.trees:
            self.assertIsInstance(tree, Tree)
            self.assertEqual(tree.formats, TEST_LIBRARY_FORMATS)

        for path in TEST_PREFIX_PATHS:
            if os.path.isdir(path):
                shutil.rmtree(path)
