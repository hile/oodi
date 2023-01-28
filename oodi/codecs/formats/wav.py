"""
Codec definition for wav files
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


class Wav(Codec):
    """
    PCM Wav audio
    """
    codec_format = CodecFormat.WAV
    description = 'Waveform Audio File Format'
    default_suffix = CodecFormat.WAV.value
    suffixes = (
        CodecFormat.WAV.value,
        'wave',
    )
    mimetypes = (
        'audio/wav',
        'audio/vnd.wave',
        'audio/wave',
        'audio/x-wav',
    )
