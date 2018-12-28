
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
    'performers': ['TMCL'],
    'album': ['TALB'],
    'title': ['TIT2'],
    'genre': ['TCON'],
    'comment': ["COMM::'eng'"],
    'note': ['TXXX'],
    'description': ['TIT3'],
    'year': ['TDRC'],
    'bpm': ['TBPM'],
    'label': ['TPUB'],
    'copyright': ['WCOP'],
    'license': ['TOWN'],
    'sort_artist': ['TSOP'],
    'sort_album': ['TSOA'],
    'sort_title': ['TSOT'],
    'track_number': ['TRCK'],
    'total_tracks': ['TRCK'],
    'disk_number': ['TPOS'],
    'total_disks': ['TPOS'],
    'album_art': ['APIC:'],
}

INTERNAL_FIELDS = ()

INTEGER_FIELDS = ()

FLOAT_FIELDS = (
    'bpm',
)

BOOLEAN_FIELDS = ()
