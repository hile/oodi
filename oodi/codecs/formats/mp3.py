"""
Codec definition for mp3 files
"""
from ..constants import CodecFormat
from .base import Codec

ENCODER_ARGUMENT_DEFAULTS = {
    'afconvert': {
        'defaults': {
            'bitrate': 320,
        }
    },
    'lame': {
        'choices': {
            'bitrate': [64, 128, 192, 256, 320],
        },
        'defaults': {
            'bitrate': 320,
        }
    }
}


class Mp3(Codec):
    """
    MPEG-2 mp3 codec
    """
    codec_format = CodecFormat.MP3
    description = 'MPEG-2 Audio Layer III'
    default_suffix = CodecFormat.MP3.value
    suffixes = (
        CodecFormat.MP3.value,
    )
    mimetypes = (
        'audio/mpeg',
        'audio/MPA',
        'audio/mpa-robust',
    )
