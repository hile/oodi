
import os

from .exceptions import LibraryError


class FilesystemItem:
    """
    Common filesystem item base class
    """

    def __init__(self, configuration, path):
        self.configuration = configuration
        self.path = os.path.expandvars(os.path.expanduser(path))

    def __repr__(self):
        return self.path

    def __stat__(self):
        """
        Try to stat item
        """
        try:
            return os.stat(self.path)
        except Exception as e:
            raise LibraryError('Error running stat on {}: {}'.format(self.path, e))

    @property
    def uid(self):
        return self.__stat__().st_uid

    @property
    def gid(self):
        return self.__stat__().st_gid

    @property
    def atime(self):
        return self.__stat__().st_atime

    @property
    def ctime(self):
        return self.__stat__().st_ctime

    @property
    def mtime(self):
        return self.__stat__().st_mtime


class Directory(FilesystemItem):
    """
    Iterable directory base class
    """

    # Ignore these filesystem metadata names
    ignored_tree_folder_names = (
        '.fseventsd',
        '.Spotlight-V100',
        '.DocumentRevisions-V100',
        '.Trashes',
        '.vol',
        '__pycache__',
    )
    # File extensions always ignored during iterator
    ignored_filenames = (
        '.DS_Store',
    )

    def __init__(self, configuration, path, iterable='files'):
        """
        Initialize iterable directory

        Argument iterable must be name of the attribute being iterated, in this implementation
        'directories' or 'files' unless class is extended to do something else.
        """
        super().__init__(configuration, path)

        self.path = os.path.expandvars(os.path.expanduser(path))
        self.__iterable__ = iterable
        self.reset()

    def __iter__(self):
        return self

    def __len__(self):
        """
        Return number of iterable items

        May return incomplete value is full tree is not yet loaded
        """
        return len(self.__get_iterable__())

    def __get_iterable__(self):
        """
        Return iterable field from object
        """
        iterable = getattr(self, self.__iterable__, None)
        if iterable is None:
            raise ValueError('Unknown iterable type: {}'.format(self.__iterable__))

        if not isinstance(iterable, list):
            raise ValueError('Attribute {} is not a list'.format(self.__iterable__))

        return iterable

    def __load_next__(self):
        """
        Load next iterable item
        """
        def get_next_slice():
            """
            Get next slice from os.walk and add directories / files to tree

            Iterator will raise StopIteration when all is processed.
            """
            try:
                root, dirs, files = next(self.__iterator__)
                dirs.sort()
            except StopIteration:
                self.__index__ = None
                self.__loaded__ = True
                raise StopIteration

            if os.path.basename(root) not in self.ignored_tree_folder_names:
                for directory in dirs:
                    self.add_directory(root, directory)
                for filename in sorted(files):
                    self.add_file(root, filename)

        if self.__iterator__ is None:
            self.__index__ = 0
            self.__iterator__ = os.walk(self.path, followlinks=True)
            get_next_slice()

        try:
            item = self.__get_iterable__()[self.__index__]
        except IndexError:
            get_next_slice()
            return self.__load_next__()

        self.__index__ += 1
        return item

    def __next__(self):
        """
        Directory iterator.

        On first round loads directory from disk as generator.

        After that, use directories and files stored to object without reloading.
        """

        if self.__loaded__ is False:
            return self.__load_next__()

        else:
            if self.__index__ is None:
                self.__index__ = 0

            try:
                item = self.__get_iterable__()[self.__index__]
            except IndexError:
                self.__index__ = 0
                raise StopIteration

            self.__index__ += 1
            return item

    @property
    def exists(self):
        """
        Check if directory exists
        """
        return os.path.isdir(self.path)

    @property
    def relative_path(self):
        """
        Return path relative to root of tree
        """
        root = self.parent
        while True:
            if root.parent:
                root = root.parent
            else:
                break
        return self.path[len(root.path) + 1:]

    def add_directory(self, root, directory):
        """
        Add directory to tree if valid.

        Override in child class as necessary.
        """
        if directory in self.ignored_tree_folder_names:
            return

        item = Directory(self.configuration, os.path.join(root, directory), iterable=self.__iterable__)
        self.__directory_index__[item.path] = item
        if root in self.__directory_index__:
            item.parent = self.__directory_index__[root]
        self.directories.append(item)

    def add_file(self, root, filename):
        """
        Add file to tree if valid.

        Override in child class as necessary.
        """
        if filename in self.ignored_filenames:
            return

        item = File(self.configuration, os.path.join(root, filename))
        if root in self.__directory_index__:
            item.parent = self.__directory_index__[root]
        self.files.append(item)

    def reset(self):
        """
        Reset loaded data to empty defaults
        """

        self.__directory_index__ = {self.path: self}
        self.parent = None
        self.directories = []
        self.files = []

        self.__loaded__ = False
        self.__iterator__ = None
        self.__index__ = None

    def load(self):
        """
        Load all items in the tree instaed of iterating
        """
        self.reset()

        while True:
            try:
                next(self)
            except StopIteration:
                break


class File(FilesystemItem):
    """
    File in library
    """
    pass


class Libraries:
    """
    Loader for configured libraries
    """

    def __init__(self, configuration):
        self.configuration = configuration
        self.trees = []
        self.__initialize_trees__()

    def __initialize_trees__(self):
        """
        Return configured trees
        """
        for item in self.configuration.library.get('trees', []):
            prefixes = item.get('prefixes', [])
            if prefixes:
                # Load directories matching prefixes
                for path in prefixes:
                    path = os.path.realpath(os.path.expandvars(os.path.expanduser(path)))
                    if os.path.isdir(path):
                        self.add_tree(
                            path,
                            formats=item.get('formats', None),
                            description=item.get('description', None),
                        )
            elif item.get('path', None):
                self.add_tree(
                    item['path'],
                    formats=item.get('formats', None),
                    description=item.get('description', None),
                )

    def add_tree(self, path, description=None, formats=list):
        """
        Add tree to libraries configuration
        """
        from oodi.library.tree import Tree

        for item in self.trees:
            if item.path == path:
                raise LibraryError('Tree already in library: {}'.format(path))

        self.trees.append(Tree(
            self.configuration,
            path,
            'files',
            formats=formats,
            description=description,
        ))

    def remove_tree(self, path):
        """
        Remove tree from libraries configuration

        Does not remove any directorieos or files in filesystem
        """
        matches = []
        for tree in self.trees:
            if tree.path == path:
                matches.append(tree)
                self.trees.remove(tree)

        if not matches:
            raise LibraryError('Tree was found not in library: {}'.format(path))

    def find_tree_by_prefix(self, path):
        """
        Return tree matching specified prefix
        """
        path = os.path.realpath(os.path.expandvars(os.path.expanduser(path)))
        for tree in self.trees:
            prefix = '{}/'.format(tree.path)
            if path[:len(prefix)] == prefix:
                return tree

    def find_trees_by_codec(self, name):
        """
        Find trees matching specified codec name

        Multiple trees may be returned
        """
        trees = []
        for tree in self.trees:
            if name in tree.formats:
                trees.append(tree)
        return trees
