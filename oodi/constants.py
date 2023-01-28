"""
Oodi configuration constants
"""
from pathlib import Path

USER_CONFIG_DIRECTORY = Path('~/.config/oodi').expanduser().resolve()
OODI_CONFIG_FILE = 'oodi.yml'

DEFAULT_FILESYSTEM_ENCODING = 'UTF-8'
