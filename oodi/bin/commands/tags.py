
from oodi.library.base import IterableFilesystemPath, LibraryError
from .base import Command


class Tags(Command):
    """
    Tags information
    """

    name = 'tags'
    short_description = 'Audio file tags processing'

    def __register_arguments__(self, parser):
        subparsers = parser.add_subparsers()

        p = subparsers.add_parser('list', help='List tags in files')
        p.add_argument('paths', nargs='*', help='Filenames to process')
        p.set_defaults(func=self.list_tags)

        p = subparsers.add_parser('magic', help='Show file magic strings')
        p.add_argument('paths', nargs='*', help='Filenames to process')
        p.set_defaults(func=self.list_magic_strings)

        p = subparsers.add_parser('set', help='List tags in files')
        p.add_argument('-t', '--tags', action='append', help='Tags to set as key=value')
        p.add_argument('paths', nargs='*', help='Filenames to process')
        p.set_defaults(func=self.set_tags)

        p = subparsers.add_parser('fix-itunes-containers', help='Fix old itunes container')
        p.add_argument('paths', nargs='*', help='Paths to process')
        p.set_defaults(func=self.fix_itunes_containers)

    def get_path_iterators(self, paths):
        iterators = []
        for path in paths:
            try:
                iterators.append(IterableFilesystemPath(self.script.configuration, path))
            except LibraryError as e:
                self.error(e)
        return iterators

    def set_tags(self, args):
        updated_tags = {}
        for arg in args.tags:
            try:
                tag, value = arg.split('=', 1)
                updated_tags[tag] = value
            except Exception:
                self.exit(1, 'Error parsing tag {}'.format(arg))

        for iterator in self.get_path_iterators(args.paths):
            for item in iterator:
                tags = self.codecs.get_tags_for_filename(item.path)
                if tags:
                    tags.update(**updated_tags)

    def list_tags(self, args):
        for iterator in self.get_path_iterators(args.paths):
            for item in iterator:
                tags = self.codecs.get_tags_for_filename(item.path)
                if tags:
                    print(tags.items())

    def list_magic_strings(self, args):
        for iterator in self.get_path_iterators(args.paths):
            for item in iterator:
                tags = self.codecs.get_tags_for_filename(item.path)
                if tags:
                    print('{}: {}'.format(item.path, tags.magic(item.path)))

    def fix_itunes_containers(self, args):
        for iterator in self.get_path_iterators(args.paths):
            for item in iterator:
                path = item.path
                tags = self.codecs.get_tags_for_filename(path)
                if tags:
                    if tags.requires_aac_itunes_fix(path):
                        print('FIX  {}'.format(path))
                        tags.fix_aac_for_itunes(path)
                    else:
                        print('OK   {}'.format(path))

    def run(self, args):
        args.func(args)
