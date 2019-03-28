
from ..cli import OodiShellCommandParser


class AlbumArt(OodiShellCommandParser):
    """
    Album art file processor
    """

    extensions = (
        'jpg',
        'png',
        'jpeg',
    )
