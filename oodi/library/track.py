
import os
import re

from . import File

# Regexp patterns to match track filenames
TRACKNAME_PATTERNS = (
    r'(?P<track_number>\d+)/(?P<total_tracks>\d+) (?P<name>.*)\.(?P<extension>[\w\d]+)$',
    r'(?P<track_number>\d+) (?P<name>.*)\.(?P<extension>[\w\d]+)$',
    r'(?P<name>.*)\.(?P<extension>[\w\d]+)$',
)


class Track(File):
    """
    Audio file track in tree
    """

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', None)
        super().__init__(*args, **kwargs)

        self.track_number = None
        self.total_tracks = None
        self.name = None
        self.extension = None
        self.__parse_details_from_filename__()

        self.__tagparser__ = None
        self.__tree__ = None

    def __parse_details_from_filename__(self):
        """
        Parse track details from filename
        """

        patterns = [re.compile(pattern) for pattern in TRACKNAME_PATTERNS]
        directory = os.path.dirname(self.path)
        filename = os.path.basename(self.path)

        for pattern in patterns:
            m = pattern.match(filename)
            if m:
                for attr, value in m.groupdict().items():
                    if attr == 'track_number':
                        value = int(value)
                    setattr(self, attr, value)
                break

        # Guess number of total tracks in directory
        if self.total_tracks is None:
            total_tracks = 0
            for filename in os.listdir(directory):
                if os.path.splitext(filename)[1][1:] == self.extension:
                    total_tracks += 1
            self.total_tracks = total_tracks

    @property
    def tree(self):
        """
        Find library tree based on path
        """
        if self.__tree__ is None:
            self.__tree__ = self.configuration.library.find_tree_by_prefix(self.path)
        return self.__tree__

    @property
    def relative_path(self):
        """
        Return relative path to library

        Raises ValueError if file is not linked to a tree
        """
        if self.tree is not None:
            prefix = '{}/'.format(self.tree.path)
            return self.path[len(prefix):].lstrip('/')
        else:
            raise ValueError('File {} is not linked to a tree'.format(self.path))

    @property
    def codec(self):
        """
        Get codec for file based on filename extension
        """
        from oodi.codecs.utils import detect_file_codec
        if self.format:
            codecs = self.configuration.codecs.codecs
            for codec in codecs:
                if codec.format == self.format:
                    return codec
            raise ValueError('Unknown format: {}'.format(self.format))
        elif self.extension:
            codecs = self.configuration.codecs.find_codecs_for_extension(self.extension)
            if len(codecs) == 1:
                return codecs[0]
            else:
                tree = self.tree
                if tree is not None:
                    return tree.codec
                else:
                    self.format = detect_file_codec(self.path)
                    if self.format is not None:
                        codecs = self.configuration.codecs.codecs
                        for codec in codecs:
                            if codec.format == self.format:
                                return codec
                    raise ValueError('Extension {} matches multiple codecs'.format(self))
        else:
            raise ValueError('Filename has no extension:{}'.format(self.path))

    @property
    def tags(self):
        if self.__tagparser__ is None:
            self.__tagparser__ = self.codec.tagparser
            self.__tagparser__.load(self.path)
        return self.__tagparser__

    @property
    def length(self):
        """
        Return length of file as float
        """
        return self.tags.info['length']

    @property
    def bitrate(self):
        """
        Return file bitrate as integer
        """
        return self.tags.info['bitrate']

    @property
    def channels(self):
        """
        Return number of audio channels
        """
        return self.tags.info['channels']

    @property
    def bits_per_sample(self):
        """
        Return file sample bit depth (16, 24 etc)
        """
        for attr in ('bits_per_sample', 'sample_size'):
            if attr in self.tags.info:
                return self.tags.info[attr]
        return None

    @property
    def sample_rate(self):
        """
        Return file sample rate (44100, 48000 etc)
        """
        return self.tags.info['sample_rate']

    def decode(self, output_file=None, *args, **kwargs):
        """
        Decode file to specified output file
        """
        decoder = self.codec.decoder
        if decoder:
            return decoder.decode(self.path, output_file, *args, **kwargs)
        else:
            raise ValueError('Codec has no decoder')

    def encode(self, input_file, *args, **kwargs):
        """
        Encode specified file to track path
        """
        encoder = self.codec.encoder
        if encoder:
            return encoder.encode(input_file, self.path, *args, **kwargs)
        else:
            raise ValueError('Codec has no encoder')

    def test(self, *args, **kwargs):
        """
        Run format tester for file
        """
        tester = self.codec.tester
        if tester:
            return tester.test(self.path, *args, **kwargs)
        else:
            raise ValueError('Codec has no tester')
