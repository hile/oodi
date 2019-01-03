
import os

from mutagen.mp3 import MP3
from mutagen.id3 import ID3

from ...codecs import BaseTagParser, ValueTotalCountTag
from .constants import TAG_FIELDS


class Mp3ValueTotalTag(ValueTotalCountTag):
    """
    MP3 value total track argument pairs
    """
    field = None

    def get(self):
        """
        Get MP3 numbering details
        """
        try:
            data = self.parser.__entry__[self.field].text[0].split('/')
            self.value = int(data[0])
            self.total = int(data[1])
        except KeyError:
            self.value = None
            self.total = None

    def save(self):
        """
        Save MP3 numbering details
        """
        if self.total is not None:
            value = '{}/{}'.format(self.value, self.total)
        else:
            value = '{}/{}'.format(self.value, self.value)

        self.parser.__entry__[self.field] = self.parser.__format_tag__(self.numbering_tag, value)
        self.parser.__entry__.save()


class MP3TrackNumberingTag(Mp3ValueTotalTag):
    numbering_tag = 'track_number'
    field = 'TRKN'


class MP3DiskNumberingTag(Mp3ValueTotalTag):
    numbering_tag = 'disk_number'
    field = 'TPOS'


class TagParser(BaseTagParser):
    """
    MP3 tag processor
    """
    format = 'mp3'
    loader = MP3
    fields = TAG_FIELDS
    track_numbering_class = MP3TrackNumberingTag
    disk_numbering_class = MP3DiskNumberingTag

    def __getattr__(self, attr):
        """
        Get mp3 tag attribute and decode frame
        """
        value = super().__getattr__(attr)
        if value is not None:
            return value.text[0]
        return value

    def __format_tag__(self, tag, value):
        """
        Format tag as MP3 frame for saving
        """
        from mutagen.id3._specs import Encoding

        if not isinstance(value, list):
            value = [value]

        try:
            field = self.fields[tag][0]
            m = __import__('mutagen.id3', globals(), {}, tag)
            frame = getattr(m, field)
            if frame is None:
                raise AttributeError
            return frame(encoding=Encoding.UTF8, text=value)
        except AttributeError as e:
            raise ValueError('Error importing ID3 frame {}: {}'.format(tag, e))

    def load(self, path):
        self.__path__ = path
        self.__entry__ = self.loader(
            os.path.expandvars(os.path.expanduser(path)),
            ID3=ID3
        )
