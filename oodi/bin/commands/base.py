
from systematic.shell import ScriptCommand

from oodi.codecs.base import Codecs
from oodi.library.base import Libraries


class Command(ScriptCommand):
    """
    Common base class for Oodi CLI commands
    """

    @property
    def codecs(self):
        """
        Return codecs with current configurtion
        """
        return Codecs(configuration=self.script.configuration)

    @property
    def libraries(self):
        return Libraries(configuration=self.script.configuration)
