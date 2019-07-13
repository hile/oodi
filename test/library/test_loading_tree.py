
import unittest

TEST_TREE_PATH = '/tmp'


class TreeLoadingTests(unittest.TestCase):
    """
    Tests loading of oodi library tree objects
    """

    def test_loading_tree_without_configuration(self):
        from oodi.configuration import Configuration
        from oodi.library.tree import Tree
        tree = Tree(TEST_TREE_PATH)
        self.assertIsInstance(tree.configuration, Configuration)

    def test_loading_tree_with_configuration(self):
        from oodi.configuration import Configuration
        from oodi.library.tree import Tree

        tree = Tree(TEST_TREE_PATH, Configuration())
        self.assertIsInstance(tree.configuration, Configuration)

        tree = Tree(TEST_TREE_PATH, configuration=Configuration())
        self.assertIsInstance(tree.configuration, Configuration)
