
import os
import unittest

TEST_FILES = (
    'test-aac.m4a',
    'test.aif',
    'test-alac.m4a',
    'test.caf',
    'test.flac',
    'test.ogg',
    'test.mp3',
    'test.opus',
    'test.wav',
    'test.wv'
)
TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), 'files')


class CodecDecoders(unittest.TestCase):
    """
    Tests codec decoders
    """

    def test_codec_decoders_tempfile_output(self):
        """
        Call all decoders without explicit path, decoding to temporary file
        """
        from oodi.configuration import Configuration
        from oodi.library.track import Track

        configuration = Configuration()
        for name in TEST_FILES:
            testfile = os.path.join(TEST_FILES_PATH, name)
            track = Track(configuration, testfile)
            output_file = track.decode()
            self.assertTrue(
                os.path.isfile(output_file),
                'Error decoding {}: missing output file {}'.format(testfile, output_file)
            )

    def test_codec_decoders_explicit_output_file(self):
        """
        Call all decoders by specifying a named output file path
        """
        from oodi.configuration import Configuration
        from oodi.library.track import Track

        configuration = Configuration()
        output_file = configuration.get_temporary_file_path('test.wav')
        for name in TEST_FILES:
            if os.path.isfile(output_file):
                os.unlink(output_file)
            testfile = os.path.join(TEST_FILES_PATH, name)
            track = Track(configuration, testfile)
            track.decode(output_file)
            self.assertTrue(
                os.path.isfile(output_file),
                'Error decoding {}: missing output file {}'.format(testfile, output_file)
            )
