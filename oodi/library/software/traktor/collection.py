
import lxml
import os

COLLECTION_FILENAME = 'collection.nml'


class Collection:
    """
    Traktor library collection.nml file parser
    """
    def __init__(self, application):
        self.application = application
        self.filename = os.path.join(application.directory, COLLECTION_FILENAME)

    def __repr__(self):
        return self.filename
