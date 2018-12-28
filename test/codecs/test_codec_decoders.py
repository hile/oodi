
import os
import unittest

TEST_CODEC_NAMES = (
    'aac',
    'aif',
    'alac',
    'caf',
    'flac',
    'mp3',
    'opus',
    'vorbis',
    'wav',
    'wavpack',
)
TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), 'files')


class CodecDecoders(unittest.TestCase):
    """
    Tests codec decoders
    """
