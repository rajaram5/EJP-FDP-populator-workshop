class Resource:

    TYPE = None
    TITLE = None
    DESCRIPTION = None
    KEYWORDS = []
    PUBLISHER_NAME = None
    CATALOG = None
    THEMES = []

    def __init__(self, type, title, description, publisher, keywords, themes, catalog):
        self.TYPE = type
        self.TITLE = title
        self.DESCRIPTION = description
        self.PUBLISHER_NAME = publisher
        self.CATALOG = catalog
        self.KEYWORDS = keywords
        self.THEMES = themes