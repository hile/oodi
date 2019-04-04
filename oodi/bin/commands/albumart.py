
from .base import Command
from ...metadata.albumart import AlbumArt, detect_album_art


class AlbumartCommand(Command):
    """
    Album art information
    """

    name = 'albumart'
    short_description = 'Audio file album art processing'

    def __register_arguments__(self, parser):
        subparsers = parser.add_subparsers()

        p = subparsers.add_parser('embed', help='Embed albumart in files')
        p.add_argument('-a', '--albumart', help='Album art to embed')
        p.add_argument('paths', nargs='*', help='Filenames to process')
        p.set_defaults(func=self.embed_albumart)

    def embed_albumart(self, args):
        if args.albumart:
            albumart = AlbumArt(self.script.configuration, args.albumart)

        for arg in self.get_tracks(args.paths):
            for track in arg:
                tags = track.tags
                if tags:
                    if not args.albumart:
                        albumart = detect_album_art(self.script.configuration, track.path)
                        if albumart is None:
                            continue
                    tags.set_albumart(albumart)
