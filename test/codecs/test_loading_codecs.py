
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
TEST_NO_TAGPARSER = (
    'caf',
    'wav',
)
TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), 'files')


class CodecLoading(unittest.TestCase):
    """
    Tests loading of codecs
    """

    def test_loaders_codecs(self):
        """
        Test loading codec objects (oodi.codecs.Codecs)
        """
        from oodi.configuration import Configuration
        from oodi.codecs.base import Codecs, CodecError, GenericAudioFile, BaseDecoder, BaseEncoder, BaseTagParser

        codecs = Codecs(Configuration())

        # Test accessing common codec objects by name
        for name in TEST_CODEC_NAMES:
            codec = getattr(codecs, name)
            self.assertIsInstance(codec, GenericAudioFile)

            self.assertIsInstance(codec.encoder, BaseEncoder)
            self.assertEqual(codec.format, codec.encoder.format, 'Codec encoder format mismatch: {}'.format(
                codec.format,
                codec.encoder.format,
            ))

            self.assertIsInstance(codec.decoder, BaseDecoder)
            self.assertEqual(codec.format, codec.decoder.format, 'Codec decoder format mismatch: {}'.format(
                codec.format,
                codec.decoder.format,
            ))

            if name in TEST_NO_TAGPARSER:
                with self.assertRaises(CodecError):
                    codec.tagparser
            else:
                self.assertIsInstance(codec.tagparser, BaseTagParser)
                self.assertEqual(codec.format, codec.tagparser.format, 'Codec tag parser format mismatch: {}'.format(
                    codec.format,
                    codec.tagparser.format,
                ))
