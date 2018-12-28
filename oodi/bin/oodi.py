
from systematic.shell import Script, ScriptCommand

from oodi.configuration import Configuration, ConfigurationError, DEFAULT_CONFIG_PATH


USAGE = """Oodi music library management tool

"""


class OodiScript(Script):
    """
    Custom script for oodi
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument('-c', '--config', default=DEFAULT_CONFIG_PATH, help='Configuration file')

    def __process_args__(self, args):
        try:
            self.configuration = Configuration(args.config)
        except ConfigurationError as e:
            self.exit(1, e)
        return super().__process_args__(args)


class Command(ScriptCommand):
    """
    Commands for Oodi
    """
    pass


def main():
    script = OodiScript(USAGE)
    script.parse_args()


if __name__ == '__main__':
    main()
