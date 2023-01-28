"""
Codec definition for aac files
"""
from ..constants import CodecFormat
from .base import Codec

ENCODER_ARGUMENT_DEFAULTS = {
    'oggenc': {
        'choices': {
            'quality': range(1, 9),
        },
        'defaults': {
            'quality': 8,
        }
    }
}


class Vorbis(Codec):
    """
    Ogg vorbis audio
    """
    codec_format = CodecFormat.VORBIS
    description = 'Ogg Vorbis'
    default_suffix = CodecFormat.VORBIS.value
    suffixes = (
        CodecFormat.VORBIS.value,
        'vorbis',
    )
    mimetypes = (
        'application/ogg',
        'audio/ogg',
        'audio/vorbis',
        'audio/vorbis-config',
    )
