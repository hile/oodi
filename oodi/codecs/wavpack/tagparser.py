
from mutagen.wavpack import WavPack

from ...codecs import BaseTagParser, ValueTotalCountTag


class WavpackTotalCountTag(ValueTotalCountTag):
    """
    Count / value tags for wavpack
    """
    pass


class TagParser(BaseTagParser):
    """
    Wavpack tag processor
    """

    format = 'wavpack'
    loader = WavPack
    track_numbering_class = WavpackTotalCountTag
    disk_numbering_class = WavpackTotalCountTag
