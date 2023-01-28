"""
Codec definition for alac files
"""
from ..constants import CodecFormat
from .base import Codec

ENCODER_ARGUMENT_DEFAULTS = {
    'afconvert': {
        'choices': {},
        'defaults': {},
    }
}


class Alac(Codec):
    """
    Apple ALAC audio
    """
    codec_format = CodecFormat.ALAC
    description = 'Apple Lossless Audio Codec'

    default_suffix = CodecFormat.ALAC.value
    suffixes = (
        CodecFormat.ALAC.value,
        'm4a'
    )
