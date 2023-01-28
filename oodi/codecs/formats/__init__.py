"""
Codec file formats
"""
# flake8: noqa: F401
from .aac import Aac
from .aiff import Aiff
from .alac import Alac
from .caf import Caf
from .flac import Flac
from .mp3 import Mp3
from .opus import Opus
from .vorbis import Vorbis
from .wav import Wav
from .wavpack import Wavpack


CODECS = (
    Aac,
    Aiff,
    Alac,
    Caf,
    Flac,
    Mp3,
    Opus,
    Vorbis,
    Wav,
    Wavpack,
)
