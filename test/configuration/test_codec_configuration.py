
import os
import unittest

TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), 'files')


class CodecConfigurationTests(unittest.TestCase):
    """
    Tests loading of oodi configuration
    """
