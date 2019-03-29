
from oodi.codecs.mp4.tagparser import MP4TagParser

ITUNES_BROKEN_AAC_MAGIC = 'ISO Media, MP4 v2 [ISO 14496-14]'
ITUNES_EXPECTED_AAC_MAGIC = 'ISO Media, Apple iTunes ALAC/AAC-LC (.M4A) Audio'


class TagParser(MP4TagParser):
    """
    AAC tag processor
    """

    format = 'aac'

    def requires_aac_itunes_fix(self, path):
        return self.magic(path) == ITUNES_BROKEN_AAC_MAGIC

    def fix_aac_for_itunes(self, path):
        """
        Fix old AAC files for itunes

        Old files no more playing have magic 'ISO Media, MP4 v2 [ISO 14496-14]'
        """
        from shutil import copyfile
        from subprocess import check_output

        magic = self.magic(path)

        # Already correct magic
        if magic == ITUNES_EXPECTED_AAC_MAGIC:
            return

        # Check this is actually of broken type
        if magic != ITUNES_BROKEN_AAC_MAGIC:
            print('{} unexpected magic string: {}'.format(path, magic))
            return

        # Get tag items to process to be added back to corrected file
        tags = self.items()

        # Copy file to /tmp for processing
        copyfile(path, '/tmp/broken.m4a')

        # Use afconvert to create new file. This will have correct container type
        check_output((
            'afconvert',
            '-b', '256000',
            '-f', 'm4af',
            '-d', 'aac',
            '--soundcheck-generate',
            '/tmp/broken.m4a',
            '/tmp/fixed.m4a'
        ))

        # Add existing tags back to fixed file
        self.load('/tmp/fixed.m4a')
        self.update(**tags)

        # Copy fixed file back in place
        copyfile('/tmp/fixed.m4a', path)
