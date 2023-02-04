"""
Oodi audio file album art images
"""
from .base import Metadata

PIL_EXTENSION_MAP = {
    'JPEG':     'jpg',
    'PNG':      'png',
}

PIL_MIMETYPE_MAP = {
    'JPEG':     'image/jpeg',
    'PNG':      'image/png',
}


# pylint# pylint: disable=too-few-public-methods
class AlbumArt(Metadata):
    """
    Album art metadata files
    """
