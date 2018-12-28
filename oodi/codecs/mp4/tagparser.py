
from mutagen.mp4 import MP4
# These will be needed for coverart handling MP4Cover, MP4StreamInfoError, MP4MetadataValueError

from oodi.codecs import BaseTagParser, ValueTotalCountTag
from oodi.codecs.mp4.constants import TAG_FIELDS, INTERNAL_FIELDS


class MP4ValueTotalTag(ValueTotalCountTag):
    """
    AAC value/total pair tags
    """

    def get(self):
        try:
            self.value, self.total = self.parser.__entry__[self.tag][0]
        except KeyError:
            self.value = None
            self.total = None


class MP4TagParser(BaseTagParser):
    """
    MP4 container tag processor
    """

    supports_album_art = True
    loader = MP4
    fields = TAG_FIELDS
    internal_fields = INTERNAL_FIELDS
    track_numbering_class = MP4ValueTotalTag
    disk_numbering_class = MP4ValueTotalTag
    track_numbering_tag = 'trkn'
    disk_numbering_tag = 'disk'
