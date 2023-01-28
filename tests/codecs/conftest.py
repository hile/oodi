"""
Unit test configuration specific to oodi.codecs module
"""
import itertools

from pathlib import Path
from typing import Iterable

import pytest

from oodi.codecs.constants import CodecFormat
from oodi.codecs.formats import CODECS

VALID_SUFFIXES = sorted(set(itertools.chain(*[codec.suffixes for codec in CODECS])))
VALID_MIMETYPES = sorted(set(itertools.chain(*[codec.mimetypes for codec in CODECS])))


@pytest.fixture(params=CodecFormat)
def mock_codec_format(request) -> Iterable[Path]:
    """
    Generator for lists of valid codec formats
    """
    yield request.param


@pytest.fixture(params=VALID_MIMETYPES)
def mock_codec_mimetype(request) -> Iterable[str]:
    """
    Generator for lists of valid mimetypes for codecs
    """
    yield request.param


@pytest.fixture(params=VALID_SUFFIXES)
def mock_codec_filename(request) -> Iterable[Path]:
    """
    Generator for lists of valid filenames for codecs
    """
    yield Path(f'01 Test audio file.{request.param}')
