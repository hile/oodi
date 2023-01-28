"""
Codec definition for wavpack files
"""
from ..constants import CodecFormat
from .base import Codec

ENCODER_ARGUMENT_DEFAULTS = {
    'wavpack': {
        'choices': {},
        'defaults': {}
    }
}


class Wavpack(Codec):
    """
    Wavpack audio
    """
    codec_format = CodecFormat.WAVPACK
    description = 'Wavpack files'
    default_suffix = CodecFormat.WAVPACK.value
    suffixes = (
        CodecFormat.WAVPACK.value,
        'wavpack',
    )
    mimetypes = ()
