"""
Constants for Oodi audio file metadata
"""
import itertools
from enum import Enum


class AlbumartFormat(Enum):
    """
    Supported formats for AlbumArt files
    """
    JPEG = 'jpg'
    PNG = 'png'
    GIF = 'gif'


class BookletFormat(Enum):
    """
    Supported formats for Booklet files
    """
    PDF = 'pdf'


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
BOOKLET_EXTENSION_FORMAT_MAP = {
    BookletFormat.PDF: (
        '.pdf',
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
BOOKLET_BASE_NAMES = (
    'booklet',
)

DEFAULT_ALBUMART_FILENAME = (
    f'{ALBUMART_BASE_NAMES[0]}'
    f'{ALBUMART_EXTENSION_FORMAT_MAP[AlbumartFormat.PNG][0]}'
)
DEFAULT_BOOKLET_FILENAME = (
    f'{BOOKLET_BASE_NAMES[0]}'
    f'{BOOKLET_EXTENSION_FORMAT_MAP[BookletFormat.PDF][0]}'
)

ALBUMART_FILENAME_SUFFIXES = list(
    itertools.chain(*[
        list(extensions)
        for extensions in ALBUMART_EXTENSION_FORMAT_MAP.values()
    ])
)
BOOKLET_FILENAME_SUFFIXES = list(
    itertools.chain(*[
        list(extensions)
        for extensions in BOOKLET_EXTENSION_FORMAT_MAP.values()
    ])
)

ALBUMART_SUPPORTED_FILENAMES = list(
    f'{name}{suffix}'
    for name in ALBUMART_BASE_NAMES for suffix in ALBUMART_FILENAME_SUFFIXES
)
BOOKLET_SUPPORTED_FILENAMES = list(
    f'{name}{suffix}'
    for name in BOOKLET_BASE_NAMES for suffix in BOOKLET_FILENAME_SUFFIXES
)
