
ALBUMART_MIME_TYPES = {
    'JPEG':     'image/jpeg',
    'PNG':      'image/png'
}

TAG_FIELDS = {
    'album_artist': ['TIT1'],
    'artist': ['TPE1'],
    'composer': ['TCOM'],
    'conductor': ['TPE3'],
    'orchestra': ['TPE2'],
    'album': ['TALB'],
    'title': ['TIT2'],
    'genre': ['TCON'],
    'comment': ['COMM'],
    'description': ['TIT3'],
    'year': ['TDRC'],
    'bpm': ['TBPM'],
    'label': ['TPUB'],
    'sort_artist': ['TSOP'],
    'sort_album': ['TSOA'],
    'sort_title': ['TSOT'],
    'track_number': ['TRCK'],
    'total_tracks': ['TRCK'],
    'disk_number': ['TPOS'],
    'total_disks': ['TPOS'],
    'album_art': ['APIC:'],
    # Disabled due to complex encoding not implemented yet
    # 'copyright': ['WCOP'],
    # 'license': ['TOWN'],
    # 'note': ['TXXX'],
    # 'performer': ['TMCL'],
}

INTERNAL_FIELDS = ()

INTEGER_FIELDS = ()

FLOAT_FIELDS = (
    'bpm',
)

BOOLEAN_FIELDS = ()
