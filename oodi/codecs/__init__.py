
import os

from .. import OodiShellCommandParser


class CodecError(Exception):
    """
    Exceptions from codecs and codec commands
    """
    pass


class AudiofileProcessorBaseClass(OodiShellCommandParser):
    """
    Base class for audio file processors
    """
    format = None
    commands = ()

    def __repr__(self):
        return self.format


class CommandArgumentParser:
    """
    Process command argument defaults
    """
    defaults = {}
    choices = {}
    args = ()

    def __call__(self, callback):
        kwargs = {}
        for arg in self.args:
            value = getattr(callback, arg, None)
            default = self.defaults.get(arg, None)
            value = value if value is not None else default
            if value is not None:
                self.validate(arg, value)
            kwargs[arg] = value
        return kwargs

    def validate(self, arg, value):
        """
        Validator for fields.

        Implement in child class
        """
        if arg in self.choices:
            if value not in self.choices[arg]:
                raise ValueError('Invalid value: {}'.format(value))


class BaseDecoder(AudiofileProcessorBaseClass):
    """
    Base class for audio file decoders
    """
    def commands(self):
        return self.configuration.codecs.get('decoders', {}).get(self.format, [])

    def decode(self, input_file, output_file=None, **kwargs):
        """
        Run decoder for specified file
        """

        if output_file is None:
            output_file = self.configuration.get_temporary_file_path(suffix='.wav')

        kwargs.update({
            'inputfile': input_file,
            'outputfile': output_file,
        })
        args = self.__parse_command__(**kwargs)
        self.execute(args)
        return output_file


class BaseEncoder(AudiofileProcessorBaseClass):
    """
    Base class for audio file encoders
    """
    default_quality = None
    default_bitrate = None

    @property
    def quality(self):
        """
        Quality from configuration or defaults
        """
        return self.configuration.codecs.get(self.format, {}).get('quality', self.default_quality)

    @property
    def bitrate(self):
        """
        Bitrate from configuration or defaults
        """
        return self.configuration.codecs.get(self.format, {}).get('bitrate', self.default_bitrate)

    def commands(self):
        return self.configuration.codecs.get('encoders', {}).get(self.format, [])

    def encode(self, input_file, output_file=None, remove_input_file=True, **kwargs):
        """
        Run encoder for specified file
        """

        if output_file is None:
            output_file = self.configuration.get_temporary_file_path(suffix='.{}'.format(self.format))

        kwargs.update({
            'inputfile': input_file,
            'outputfile': output_file,
        })
        args = self.__parse_command__(**kwargs)
        self.execute(args)

        if remove_input_file:
            os.unlink(input_file)

        return output_file


class BaseTester(AudiofileProcessorBaseClass):
    """
    Base class for audio file testers
    """
    def commands(self):
        return self.configuration.codecs.get('testers', {}).get(self.format, [])

    def test(self, input_file):
        """
        Run format test for specified file
        """
        raise NotImplementedError


class ValueTotalCountTag:
    """
    Value / total count integer pair for data
    """
    def __init__(self, parser, tag):
        self.parser = parser
        self.tag = tag
        self.value = None
        self.total = None

    def get(self):
        raise NotImplementedError

    def set(self):
        raise NotImplementedError


class BaseTagParser(AudiofileProcessorBaseClass):
    """
    Base class for audio file tagging classes
    """

    format = None
    supports_list_fields = False
    supports_album_art = False
    loader = None
    fields = {}
    internal_fields = ()
    list_tags = ()
    track_numbering_class = ValueTotalCountTag
    disk_numbering_class = ValueTotalCountTag
    track_numbering_tag = None
    disk_numbering_tag = None

    def __init__(self, configuration):
        """
        Open tags for given file
        """
        self.configuration = configuration
        self.__path__ = None
        self.__entry__ = None
        self.track_numbering = self.track_numbering_class(self, self.track_numbering_tag)
        self.disk_numbering = self.disk_numbering_class(self, self.disk_numbering_tag)

    def __repr__(self):
        if self.__path__ is not None:
            return '{} {}'.format(self.format, self.__path__)
        else:
            return '{} no file loaded'.format(self.format)

    def __getattr__(self, attr):
        """
        Get tag by name
        """
        try:
            tag_attributes = self.fields[attr]
        except KeyError:
            raise AttributeError

        for tag_attribute in tag_attributes:
            if tag_attribute in self.__entry__.tags:
                value = self.__entry__.tags[tag_attribute]
                if attr not in self.list_tags and isinstance(value, list):
                    value = value[0]
                return value
        return None

    def __setattr__(self, attr, value):
        """
        Set tag value
        """
        if attr in self.fields:
            tag = self.fields[attr][0]
            self.__entry__[tag] = self.__format_tag__(attr, value)
            self.__entry__.save()
        else:
            super().__setattr__(attr, value)

    def __format_tag__(self, tag, value):
        """
        Format tag to internal tag presentation
        """
        return value

    @property
    def track_number(self):
        self.track_numbering.get()
        return self.track_numbering.value

    @property
    def total_tracks(self):
        self.track_numbering.get()
        return self.track_numbering.total

    @property
    def disk_number(self):
        self.disk_numbering.get()
        return self.disk_numbering.value

    @property
    def total_disks(self):
        self.disk_numbering.get()
        return self.disk_numbering.total

    @property
    def info(self):
        """
        Return information about loaded file
        """
        if self.__path__:
            return vars(self.__entry__.info)
        else:
            return {}

    def load(self, path):
        self.__path__ = path
        self.__entry__ = self.loader(os.path.expandvars(os.path.expanduser(path)))

    def items(self, internal_fields=False):
        """
        Get all known tags
        """
        items = {}
        for field in self.fields.keys():
            if field in self.internal_fields and not internal_fields:
                continue

            value = self.__getattr__(field)
            if value is not None:
                items[field] = value

        for attr in ('track_number', 'total_tracks', 'disk_number', 'total_disks'):
            value = getattr(self, attr, None)
            if value is not None:
                items[attr] = value

        return items


class GenericAudioFile(AudiofileProcessorBaseClass):
    """
    Generic audio file base class
    """

    decoder_class = None
    encoder_class = None
    tester_class = None
    tagparser_class = None

    description = None
    extensions = ()
    mimetypes = ()

    @property
    def decoder(self):
        """
        Return decoder for audio file if available
        """
        if self.decoder_class is not None:
            return self.decoder_class(self.configuration)
        else:
            raise CodecError('Codec {} has no decoder'.format(self.format))

    @property
    def encoder(self):
        """
        Return encoder for audio file if available
        """
        if self.encoder_class is not None:
            return self.encoder_class(self.configuration)
        else:
            raise CodecError('Codec {} has no encoder'.format(self.format))

    @property
    def tagparser(self):
        """
        Return tag parsers for audio file if available
        """
        if self.tagparser_class:
            return self.tagparser_class(self.configuration)
        else:
            raise CodecError('Codec {} does not support tagging'.format(self.format))

    @property
    def tester(self):
        """
        Return tester for audio file if available
        """
        if self.tester_class is not None:
            return self.tester_class(self.configuration)
        else:
            raise CodecError('Codec {} does not support testing'.format(self.format))


class Codecs:
    """
    Supported codec implementations
    """

    def __init__(self, configuration):
        from .aac import Audiofile as AAC
        from .aif import Audiofile as AIF
        from .alac import Audiofile as ALAC
        from .caf import Audiofile as CAF
        from .flac import Audiofile as FLAC
        from .mp3 import Audiofile as MP3
        from .opus import Audiofile as OPUS
        from .vorbis import Audiofile as VORBIS
        from .wav import Audiofile as WAV
        from .wavpack import Audiofile as WAVPACK

        self.configuration = configuration
        self.codecs = (
            AAC(self.configuration),
            AIF(self.configuration),
            ALAC(self.configuration),
            CAF(self.configuration),
            FLAC(self.configuration),
            MP3(self.configuration),
            OPUS(self.configuration),
            VORBIS(self.configuration),
            WAV(self.configuration),
            WAVPACK(self.configuration),
        )

    def __getattr__(self, name):
        """
        Get codec by name of format
        """
        for codec in self.codecs:
            if codec.format == name:
                return codec
        raise AttributeError('No such codec: {}'.format(name))

    def find_codecs_for_extension(self, extension):
        """
        Return codecs that match specified extension

        May return multiple (.m4a for AAC and ALAC, for example)
        """
        return [codec for codec in self.codecs if extension in codec.extensions]
