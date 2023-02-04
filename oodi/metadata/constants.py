"""
Constants for Oodi audio file metadata
"""
import itertools
from enum import Enum


class AlbumartFormat(Enum):
    """
    Supported fomrmats for AlbumArt files
    """
    JPEG = 'jpg'
    PNG = 'png'
    GIF = 'gif'


ALBUMART_EXTENSION_FORMAT_MAP = {
    AlbumartFormat.JPEG: (
        '.jpg',
        '.jpeg',
    ),
    AlbumartFormat.PNG: (
        '.png',
    ),
    AlbumartFormat.GIF: (
        '.gif',
    )
}

ALBUMART_BASE_NAMES = (
    'artwork',
    'albumart',
    'coverart',
    'cover',
    'album',
    'front',
    'back',
)

DEFAULT_ALBUMART_FILENAME = (
    f'{ALBUMART_BASE_NAMES[0]}'
    f'{ALBUMART_EXTENSION_FORMAT_MAP[AlbumartFormat.PNG][0]}'
)

ALBUMART_FILENAME_SUFFIXES = list(
    itertools.chain(*[
        list(extensions)
        for extensions in ALBUMART_EXTENSION_FORMAT_MAP.values()
    ])
)

ALBUMART_SUPPORTED_FILENAMES = list(
    f'{name}{suffix}'
    for name in ALBUMART_BASE_NAMES for suffix in ALBUMART_FILENAME_SUFFIXES
)
