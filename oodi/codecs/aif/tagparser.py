
from mutagen.aiff import AIFF

from ...codecs import BaseTagParser


class TagParser(BaseTagParser):
    """
    AIFF tag processor
    """

    format = 'aif'
    loader = AIFF

    @property
    def info(self):
        """
        Return information about loaded file
        """
        if self.__path__:
            return vars(self.__entry__.info)
        else:
            return {}
