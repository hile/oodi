"""
Codec definition for caf files
"""
from ..constants import CodecFormat
from .base import Codec

ENCODER_ARGUMENT_DEFAULTS = {
    'afconvert': {
        'choices': {
            'sample_bits': [16, 24, 32],
        },
        'defaults': {
            'sample_bits': 24,
        }
    }
}


class Caf(Codec):
    """
    Apple Caf audio
    """
    codec_format = CodecFormat.CAF
    description = 'Core Audio Format'

    default_suffix = CodecFormat.CAF.value
    suffixes = (
        CodecFormat.CAF.value,
    )
    mimetypes = (
        'audio/x-caf',
    )
