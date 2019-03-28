
from .base import Command


class ListCodecs(Command):
    """
    List codecs
    """
    name = 'list-codecs'
    short_description = 'List known codesc'

    def run(self, args):
        for codec in self.codecs:
            print(codec)
