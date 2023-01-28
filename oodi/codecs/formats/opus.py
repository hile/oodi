"""
Codec definition for opus files
"""
from ..constants import CodecFormat
from .base import Codec

DEFAULT_BITRATE = 256
ENCODER_ARGUMENT_DEFAULTS = {
    'opusenc': {
        'choices': {
            'bitrate': [32, 64, 128, 192, 256],
        },
        'defaults': {
            'bitrate': 256,
        }
    }
}


class Opus(Codec):
    """
    Opus codec
    """
    codec_format = CodecFormat.OPUS
    description = 'Opus (RFC 6716)'
    default_suffix = CodecFormat.OPUS.value
    suffixes = (
        CodecFormat.OPUS.value,
    )
    mimetypes = (
        'audio/opus',
    )
