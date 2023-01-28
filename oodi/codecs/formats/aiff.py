"""
Codec definition for aiff files
"""
from ..constants import CodecFormat
from .base import Codec

ENCODER_ARGUMENT_DEFAULTS = {
    'afconvert': {
        'choices': {
            'sample_bits': [16, 24, 32],
        },
        'defaults': {
            'sample_bits': 16,
        }
    }
}


class Aiff(Codec):
    """
    AIFF audio
    """
    codec_format = CodecFormat.AIFF
    description = 'Audio Interchange File Format'
    default_suffix = CodecFormat.AIFF.value
    suffixes = (
        CodecFormat.AIFF.value,
        'aif',
        'aifc',
    )
    mimetypes = (
        'audio/x-aiff',
        'audio/aiff',
    )
