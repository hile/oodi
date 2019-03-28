

class Metadata:
    """
    Supported metadata file types
    """
    def __init__(self, configuration):
        from .albumart import AlbumArt

        self.configuration = configuration
        self.loaders = (
            AlbumArt(self.configuration),
        )

    def find_metadata_type_for_extension(self, extension):
        """
        Return metadata filetypes that match specified extension

        May return multiple
        """
        return [metadata for metadata in self.loaders if extension in metadata.extensions]
