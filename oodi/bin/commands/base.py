
from systematic.shell import ScriptCommand

from oodi.codecs.base import Codecs


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
