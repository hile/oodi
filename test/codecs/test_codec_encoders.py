
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


class CodecEncoders(unittest.TestCase):
    """
    Tests codec encoders
    """
    def setUp(self):
        from oodi.configuration import Configuration
        self.configuration = Configuration()
        self.input_file = os.path.join(os.path.dirname(__file__), 'files/test.wav')

    def test_encoder_aac(self):
        from oodi.codecs.utils import detect_file_codec
        from oodi.library.exceptions import LibraryError
        from oodi.library.track import Track

        filename = self.configuration.get_temporary_file_path('test.m4a')

        # Raises LibraryError because .m4a matches multiple codecs
        with self.assertRaises(LibraryError):
            track = Track(self.configuration, filename)
            output_file = track.encode(self.input_file, remove_input_file=False)

        # Specifying explicit format allows encoding
        track = Track(self.configuration, filename, format='aac')
        output_file = track.encode(self.input_file, remove_input_file=False)
        self.assertEqual(output_file, track.path)
        self.assertTrue(os.path.isfile(output_file))
        self.assertEqual(detect_file_codec(filename), 'aac')

    def test_encoder_aif(self):
        from oodi.codecs.utils import detect_file_codec
        from oodi.library.track import Track

        filename = self.configuration.get_temporary_file_path('test.aif')

        track = Track(self.configuration, filename)
        output_file = track.encode(self.input_file, remove_input_file=False)
        self.assertEqual(output_file, track.path)
        self.assertTrue(os.path.isfile(output_file))
        self.assertEqual(detect_file_codec(filename), 'aif')

    def test_encoder_alac(self):
        from oodi.codecs.utils import detect_file_codec
        from oodi.library.exceptions import LibraryError
        from oodi.library.track import Track

        filename = self.configuration.get_temporary_file_path('test.m4a')

        # Raises LibraryError because .alac matches multiple codecs
        with self.assertRaises(LibraryError):
            track = Track(self.configuration, filename)
            output_file = track.encode(self.input_file, remove_input_file=False)

        # Specifying explicit format allows encoding
        track = Track(self.configuration, filename, format='alac')
        output_file = track.encode(self.input_file, remove_input_file=False)
        self.assertEqual(output_file, track.path)
        self.assertTrue(os.path.isfile(output_file))
        self.assertEqual(detect_file_codec(filename), 'alac')

    def test_encoder_caf(self):
        from oodi.library.track import Track

        filename = self.configuration.get_temporary_file_path('test.caf')

        track = Track(self.configuration, filename)
        output_file = track.encode(self.input_file, remove_input_file=False)
        self.assertEqual(output_file, track.path)
        self.assertTrue(os.path.isfile(output_file))

    def test_encoder_flac(self):
        from oodi.codecs.utils import detect_file_codec
        from oodi.library.track import Track

        filename = self.configuration.get_temporary_file_path('test.flac')

        track = Track(self.configuration, filename)
        output_file = track.encode(self.input_file, remove_input_file=False)
        self.assertEqual(output_file, track.path)
        self.assertTrue(os.path.isfile(output_file))
        self.assertEqual(detect_file_codec(filename), 'flac')

    def test_encoder_mp3(self):
        from oodi.codecs.utils import detect_file_codec
        from oodi.library.track import Track

        filename = self.configuration.get_temporary_file_path('test.mp3')

        track = Track(self.configuration, filename)
        output_file = track.encode(self.input_file, remove_input_file=False)
        self.assertEqual(output_file, track.path)
        self.assertTrue(os.path.isfile(output_file))
        self.assertEqual(detect_file_codec(filename), 'mp3')

    def test_encoder_opus(self):
        from oodi.codecs.utils import detect_file_codec
        from oodi.library.track import Track

        filename = self.configuration.get_temporary_file_path('test.opus')

        track = Track(self.configuration, filename)
        output_file = track.encode(self.input_file, remove_input_file=False)
        self.assertEqual(output_file, track.path)
        self.assertTrue(os.path.isfile(output_file))
        self.assertEqual(detect_file_codec(filename), 'opus')

    def test_encoder_vorbis(self):
        from oodi.codecs.utils import detect_file_codec
        from oodi.library.track import Track

        filename = self.configuration.get_temporary_file_path('test.ogg')

        track = Track(self.configuration, filename)
        output_file = track.encode(self.input_file, remove_input_file=False)
        self.assertEqual(output_file, track.path)
        self.assertTrue(os.path.isfile(output_file))
        self.assertEqual(detect_file_codec(filename), 'vorbis')

    def test_encoder_wavpack(self):
        from oodi.codecs.utils import detect_file_codec
        from oodi.library.track import Track

        filename = self.configuration.get_temporary_file_path('test.wv')

        track = Track(self.configuration, filename)
        output_file = track.encode(self.input_file, remove_input_file=False)
        self.assertEqual(output_file, track.path)
        self.assertTrue(os.path.isfile(output_file))
        self.assertEqual(detect_file_codec(filename), 'wavpack')
