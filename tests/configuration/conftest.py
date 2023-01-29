"""
Unit test configuration specific to oodi.configuration module
"""
from typing import Iterator

import pytest

from oodi.codecs.constants import CodecFormat


@pytest.fixture(params=CodecFormat)
def valid_codec_format(request) -> Iterator[CodecFormat]:
    """
    Return iterator for valid codec formats as CodecFormat objects
    """
    yield request.param


@pytest.fixture(params=CodecFormat)
def valid_codec_format_name(request) -> Iterator[str]:
    """
    Return iterator for valid codec formats as CodecFormat value (str)
    """
    yield request.param.value
