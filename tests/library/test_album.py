"""
Unit tests for oodi.library.album module
"""
from ..conftest import (
    MOCK_MESSAGE,
)


def test_album_properties(mock_empty_library, mock_album_relative_path, mock_album) -> None:
    """
    Test proprties of an album object
    """
    assert isinstance(mock_album.__repr__(), str)
    assert mock_album.relative_path.relative_to(mock_empty_library) == mock_album_relative_path
    assert len(mock_album.audio_files) == 0
    assert len(mock_album.metadata) == 0

    mock_album.add_metadata_file(__file__)
    assert len(mock_album.audio_files) == 0
    assert len(mock_album.metadata) == 1


def test_album_debug_disabled(mock_album, capsys):
    """
    Test album debug method with debugging disabled
    """
    assert mock_album.library.config.__debug_enabled__ is False
    mock_album.debug(MOCK_MESSAGE, mock_album)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''


def test_album_debug_enabled(mock_album, capsys):
    """
    Test album debug method with debugging enabled
    """
    mock_album.library.config.__debug_enabled__ = True
    mock_album.debug(MOCK_MESSAGE, mock_album)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1


def test_album_error_message(mock_album, capsys):
    """
    Test album error method with debugging disabled
    """
    assert mock_album.library.config.__debug_enabled__ is False
    mock_album.error(MOCK_MESSAGE, mock_album)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1


def test_album_message_silent_disabled(mock_album, capsys):
    """
    Test album debug method with silent flag disabled
    """
    assert mock_album.library.config.__silent__ is False
    mock_album.message(MOCK_MESSAGE, mock_album)
    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == 1


def test_album_message_silent_enabled(mock_album, capsys):
    """
    Test album debug method with silent flag enabled
    """
    mock_album.library.config.__silent__ = True
    mock_album.message(MOCK_MESSAGE, mock_album)
    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''


def test_album_add_audio_file(mock_album, mock_sample_file):
    """
    Mock adding audio file to the Album object with mocked audio files
    for all supported data types
    """
    mock_album.add_audio_file(mock_sample_file)
    assert len(mock_album.audio_files) == 1

    mock_album.add_audio_file(mock_sample_file)
    assert len(mock_album.audio_files) == 1


def test_album_path_lookup_properties(mock_empty_library, mock_album_relative_path, mock_album) -> None:
    """
    Test album path lookup object methods
    """
    assert len(mock_empty_library.albums) == 0
    mock_empty_library.albums[mock_album_relative_path] = mock_album
    assert len(mock_empty_library.albums) == 1

    assert mock_empty_library.albums[mock_album_relative_path] == mock_album

    albums = list(mock_empty_library.albums)
    assert len(albums) == 1

    del mock_empty_library.albums[mock_album_relative_path]
    assert len(mock_empty_library.albums) == 0


def test_album_path_lookup_debug_disabled(mock_empty_library, capsys):
    """
    Test album path lookup debug method with debugging disabled
    """
    assert mock_empty_library.config.__debug_enabled__ is False
    mock_empty_library.albums.debug(MOCK_MESSAGE, mock_empty_library)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''


def test_album_path_lookup_debug_enabled(mock_empty_library, capsys):
    """
    Test album path lookup debug method with debugging enabled
    """
    mock_empty_library.config.__debug_enabled__ = True
    mock_empty_library.albums.debug(MOCK_MESSAGE, mock_empty_library)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1


def test_album_path_lookup_error_message(mock_empty_library, capsys):
    """
    Test album path lookup error method with debugging disabled
    """
    assert mock_empty_library.config.__debug_enabled__ is False
    mock_empty_library.albums.error(MOCK_MESSAGE, mock_empty_library)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert len(captured.err.splitlines()) == 1


def test_album_path_lookup_message_silent_disabled(mock_empty_library, capsys):
    """
    Test album path lookup debug method with silent flag disabled
    """
    assert mock_empty_library.config.__silent__ is False
    mock_empty_library.albums.message(MOCK_MESSAGE, mock_empty_library)
    captured = capsys.readouterr()
    assert captured.err == ''
    assert len(captured.out.splitlines()) == 1


def test_album_path_lookup_message_silent_enabled(mock_empty_library, capsys):
    """
    Test album path lookup debug method with silent flag enabled
    """
    mock_empty_library.config.__silent__ = True
    mock_empty_library.albums.message(MOCK_MESSAGE, mock_empty_library)
    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''
