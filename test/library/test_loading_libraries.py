
import unittest


class LibraryLoadingTests(unittest.TestCase):
    """
    Tests loading of oodi libraries
    """

    def test_loading_libraries_without_configuration(self):
        from oodi.configuration import Configuration
        from oodi.library.base import Libraries
        libraries = Libraries()
        self.assertIsInstance(libraries.configuration, Configuration)

    def test_loading_libraries_with_configuration(self):
        from oodi.configuration import Configuration
        from oodi.library.base import Libraries

        libraries = Libraries(Configuration())
        self.assertIsInstance(libraries.configuration, Configuration)

        libraries = Libraries(configuration=Configuration())
        self.assertIsInstance(libraries.configuration, Configuration)
