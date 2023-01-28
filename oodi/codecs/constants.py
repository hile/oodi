"""
Constants for audio file codecs
"""
from enum import Enum


class CodecFormat(Enum):
    """
    Enumerate various codec formats
    """
    AAC = 'AAC'
    AIFF = 'AIFF'
    ALAC = 'ALAC'
    FLAC = 'FLAC'
    MP3 = 'MP3'
    WAV = 'WAV'
    VORBIS = 'VORBIS'


COMPRESSED_FORMATS = (
    CodecFormat.AAC,
    CodecFormat.VORBIS,
    CodecFormat.MP3,
)

LOSSLESS_CODECS = (
    CodecFormat.AIFF,
    CodecFormat.ALAC,
    CodecFormat.FLAC,
    CodecFormat.WAV,
)
