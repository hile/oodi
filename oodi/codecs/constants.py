"""
Constants for audio file codecs
"""
from enum import Enum


class CodecFormat(Enum):
    """
    Enumerate various codec formats
    """
    AAC = 'm4a'
    AIFF = 'aiff'
    ALAC = 'alac'
    CAF = 'caf'
    FLAC = 'flac'
    MP3 = 'mp3'
    OPUS = 'opus'
    WAV = 'wab'
    WAVPACK = 'wv'
    VORBIS = 'ogg'
