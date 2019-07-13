
import glob
import os
import re
from pkg_resources import parse_version

from .collection import Collection

TRAKTOR_DIRECTORY_PATTERNS = (
    '~/Documents/Native Instruments/Traktor *',
)
RE_TRAKTOR_VERSIONS = (
    re.compile(r'^Traktor (?P<version>[ˆ\d.]+)$'),
)


def detect_traktor_directory():
    """
    Detect directory with latest traktor version's data
    """
    def match_version_pattern(filename):
        for pattern in RE_TRAKTOR_VERSIONS:
            m = pattern.match(filename)
            if m:
                return parse_version(m.groupdict()['version'])
        return None

    latest_version = None
    latest_directory = None

    for pattern in TRAKTOR_DIRECTORY_PATTERNS:
        for directory in glob.glob(os.path.expanduser(pattern)):
            version = match_version_pattern(os.path.basename(directory))
            if version is not None:
                if latest_version is None or version > latest_version:
                    latest_version = version
                    latest_directory = directory
    return latest_version, latest_directory


class Traktor:
    """
    Traktor application
    """
    def __init__(self):
        self.version, self.directory = detect_traktor_directory()
        self.collection = Collection(self)

    def __repr__(self):
        return 'Traktor {}'.format(self.version)
