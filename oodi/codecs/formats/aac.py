"""
Codec definition for aac files
"""
from ..constants import CodecFormat
from .base import Codec


ENCODER_ARGUMENT_DEFAULTS = {
    'afconvert': {
        'choices': {
            'quality': range(0, 128),
        },
        'defaults': {
            'bitrate': 256000,
            'quality': 127,
        }
    },
    'neroAacEnc': {
        'defaults': {
            'bitrate': 256000,
        }
    }
}


class Aac(Codec):
    """
    M4a AAC audio
    """
    codec_format = CodecFormat.AAC
    description = 'Advanced Audio Coding'
    default_suffix = CodecFormat.AAC.value
    suffixes = (
        CodecFormat.AAC.value,
        'mp4',
        'm4b',
        'm4p',
        'm4r',
        'm4v',
        '3gp',
    )
    mimetypes = (
        'audio/aac',
        'audio/aacp',
        'audio/3gpp',
        'audio/3gpp2',
        'audio/mp4',
        'audio/mp4a-latm',
        'audio/mpeg4',
        'audio/mpeg4-generic',
        'audio/x-m4a',
    )
