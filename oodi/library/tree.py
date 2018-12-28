
import os

from . import Directory
from ..codecs import Codecs
from ..metadata import Metadata

from .track import Track
from .metadata import MetadataFile


class Tree(Directory):
    """
    Audio file tree in filesystem
    """

    def __init__(self, configuration, path, iterable, formats=list, description=None):
        super().__init__(configuration, path, iterable)

        if isinstance(formats, str):
            formats = formats.split()

        self.formats = formats
        self.description = description
        self.codecs = Codecs(self.configuration)
        self.metadata = Metadata(self.configuration)
        self.metadata_files = []

    @property
    def codec(self):
        """
        Return codec used for library

        Raises ValueError if multiple codes match
        """
        if len(self.formats) == 1:
            return getattr(self.codecs, self.formats[0])
        else:
            raise ValueError('Multiple codecs configuration for tree {}'.format(self.path))

    def add_directory(self, root, directory):
        """
        Add subdirectory to tree
        """
        if directory in self.ignored_tree_folder_names:
            return

        item = Tree(self.configuration, os.path.join(root, directory), iterable=self.__iterable__)
        self.__directory_index__[item.path] = item
        if root in self.__directory_index__:
            item.parent = self.__directory_index__[root]
        self.directories.append(item)

    def add_file(self, root, filename):
        """
        Add audio file to tree

        Only files with supported extensions are loaded
        """
        if filename in self.ignored_filenames:
            return

        name, extension = os.path.splitext(filename)
        if self.codecs.find_codecs_for_extension(extension[1:]):
            item = Track(self.configuration, os.path.join(root, filename))
            if root in self.__directory_index__:
                item.parent = self.__directory_index__[root]
            self.files.append(item)

        if self.metadata.find_metadata_type_for_extension(extension[1:]):
            item = MetadataFile(self.configuration, os.path.join(root, filename))
            if root in self.__directory_index__:
                item.parent = self.__directory_index__[root]
            self.metadata_files.append(item)
