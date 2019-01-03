
import os

from mutagen.aiff import AIFF

from ...codecs import BaseTagParser, ValueTotalCountTag
from .constants import TAG_FIELDS


class AIFFValueTotalCountTag(ValueTotalCountTag):
    """
    AIFF value total track argument pairs
    """
    field = None
    numbering_tag = None

    def get(self):
        """
        Get AIFF numbering details
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
        Save AIFF numbering details
        """
        if self.total is not None:
            value = '{}/{}'.format(self.value, self.total)
        else:
            value = '{}/{}'.format(self.value, self.value)

        self.parser.__entry__[self.field] = self.parser.__format_tag__(self.numbering_tag, value)
        self.parser.__entry__.save()


class AIFFTrackNumberingTag(AIFFValueTotalCountTag):
    numbering_tag = 'track_number'
    field = 'TRKN'


class AIFFDiskNumberingTag(AIFFValueTotalCountTag):
    numbering_tag = 'disk_number'
    field = 'TPOS'


class TagParser(BaseTagParser):
    """
    AIFF tag processor
    """

    format = 'aif'
    loader = AIFF
    fields = TAG_FIELDS
    track_numbering_class = AIFFTrackNumberingTag
    disk_numbering_class = AIFFDiskNumberingTag

    @property
    def info(self):
        """
        Return information about loaded file
        """
        if self.__path__:
            return vars(self.__entry__.info)
        else:
            return {}

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
        )
