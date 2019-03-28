
import os
import shutil
import unittest

TEST_FILES = (
    'test-aac.m4a',
    'test.aif',
    'test-alac.m4a',
    'test.flac',
    'test.ogg',
    'test.mp3',
    'test.opus',
    'test.wv'
)
TEST_NO_TAGGING_SUPPORT = (
    'test.caf',
    'test.wav',
)
TEST_FILES_PATH = os.path.join(os.path.dirname(__file__), 'files')

TEST_BASIC_TAGS = {
    'album_artist': 'Testaaja, Teemu',
    'artist': 'Teemu Testaaja',
    'title': 'Tää on mun eka oma biisi',
    'comment': 'Kekkonen kommentoi'
}

# Formats for which numbering tags (value/total) always require total count as well
NUMBERING_REQUIRES_TOTAL = ('aac', 'alac', 'aif', 'mp3')


class CodecTags(unittest.TestCase):
    """
    Tests tagging for various codecs
    """

    def test_tagging_empty_testfile_tags(self):
        """
        Test reading tags from included tests files.

        Tags in test files are always empty.

        Also checks files that do not support tagging.
        """
        from oodi.codecs.base import BaseTagParser
        from oodi.configuration import Configuration
        from oodi.library.track import Track

        configuration = Configuration()

        for name in TEST_NO_TAGGING_SUPPORT:
            testfile = os.path.join(TEST_FILES_PATH, name)
            track = Track(configuration, testfile)
            self.assertIsNone(
                track.codec.tagparser_class,
                'Codec {} tagparser class is defined'.format(track.codec)
            )
            self.assertFalse(track.supports_tags, 'Track {} is not expected to support tags'.format(testfile))

        for name in TEST_FILES:
            testfile = os.path.join(TEST_FILES_PATH, name)
            track = Track(configuration, testfile)

            self.assertIsNotNone(
                track.codec.tagparser_class,
                'Codec {} tagparser class is not defined'.format(track.codec)
            )
            self.assertTrue(track.supports_tags, 'Track {} is expected to support tags'.format(testfile))
            self.assertIsInstance(track.codec.tagparser, BaseTagParser)

            self.assertIsInstance(track.tags.items(), dict, 'Track {} tags.items() is not dict'.format(testfile))
            self.assertEqual(track.tags.items(), {}, 'Track {} contains tag data'.format(testfile))

    def test_tagging_basic_tag_writing(self):
        """
        Test adding basic tags to supported files
        """
        from oodi.configuration import Configuration
        from oodi.library.track import Track

        configuration = Configuration()

        for name in TEST_FILES:
            input_file = os.path.join(TEST_FILES_PATH, name)
            tag_file = configuration.get_temporary_file_path(name)
            shutil.copyfile(input_file, tag_file)
            track = Track(configuration, tag_file)
            self.assertTrue(track.supports_tags, 'Track {} is expected to support tags'.format(tag_file))

            for tag, value in TEST_BASIC_TAGS.items():
                setattr(track.tags, tag, value)
                self.assertEqual(value, getattr(track.tags, tag))

            track = Track(configuration, tag_file)
            self.assertDictEqual(track.tags.items(), TEST_BASIC_TAGS)

            track = Track(configuration, tag_file)
            for tag in TEST_BASIC_TAGS:
                delattr(track.tags, tag)
                self.assertIsNone(getattr(track.tags, tag))

            track = Track(configuration, tag_file)
            self.assertDictEqual(track.tags.items(), {})

    def test_tagging_common_tag_writing(self):
        """
        Test writing all common tag fields with random values
        """
        from uuid import uuid4
        from oodi.codecs.constants import COMMON_TEXT_TAGS
        from oodi.configuration import Configuration
        from oodi.library.track import Track

        configuration = Configuration()

        self.maxDiff = None

        for name in TEST_FILES:
            input_file = os.path.join(TEST_FILES_PATH, name)
            tag_file = configuration.get_temporary_file_path(name)

            shutil.copyfile(input_file, tag_file)
            track = Track(configuration, tag_file)
            self.assertTrue(track.supports_tags, 'Track {} is expected to support tags'.format(tag_file))

            test_tags = {}
            for tag in COMMON_TEXT_TAGS:
                if tag in track.tags.fields:
                    test_tags[tag] = str(uuid4())

            for tag, value in test_tags.items():
                setattr(track.tags, tag, value)
                self.assertEqual(
                    value,
                    getattr(track.tags, tag),
                    'Error testing {} tag {}'.format(tag_file, tag)
                )

            track = Track(configuration, tag_file)
            self.assertDictEqual(
                track.tags.items(),
                test_tags,
                'Error comparing {} tag dictionaries'.format(tag_file)
            )

            track = Track(configuration, tag_file)
            for tag in test_tags:
                delattr(track.tags, tag)
                self.assertIsNone(getattr(track.tags, tag))

            track = Track(configuration, tag_file)
            self.assertDictEqual(track.tags.items(), {})

    def test_tagging_track_numbering_writing(self):
        """
        Test writing track numbering tags
        """
        from oodi.configuration import Configuration
        from oodi.library.track import Track

        configuration = Configuration()

        for name in TEST_FILES:
            input_file = os.path.join(TEST_FILES_PATH, name)
            tag_file = configuration.get_temporary_file_path(name)

            shutil.copyfile(input_file, tag_file)
            track = Track(configuration, tag_file)
            self.assertTrue(track.supports_tags, 'Track {} is expected to support tags'.format(tag_file))

            for value in (-1, 0, '0/0', None, '0,' '-123.3'):
                with self.assertRaises(ValueError):
                    track.tags.track_number = value

            for value in ('None/123', '11/10'):
                with self.assertRaises(ValueError):
                    track.tags.track_number = value

            shutil.copyfile(input_file, tag_file)
            track = Track(configuration, tag_file)
            track.tags.track_number = '3'
            self.assertEqual(track.tags.track_number, 3)
            if track.codec.format in NUMBERING_REQUIRES_TOTAL:
                self.assertEqual(track.tags.total_tracks, 3, 'Track {} total tracks mismatch'.format(tag_file))
            else:
                self.assertEqual(track.tags.total_tracks, None, 'Track {} total tracks mismatch'.format(tag_file))

            shutil.copyfile(input_file, tag_file)
            track = Track(configuration, tag_file)
            track.tags.track_number = '5/10'
            self.assertEqual(track.tags.track_number, 5)
            self.assertEqual(track.tags.total_tracks, 10)
