"""
Codec definition for flac files
"""
from ..constants import CodecFormat
from .base import Codec


class Flac(Codec):
    """
    FLAC audio
    """
    codec_format = CodecFormat.FLAC
    description = 'Free Lossless Audio Codec'
    default_suffix = CodecFormat.FLAC.value
    suffixes = (
        CodecFormat.FLAC.value,
    )
    mimetypes = (
        'audio/flac',
    )
