class Catalog:

    TITLE = None
    DESCRIPTION = None
    URI = None
    FDP_URL = None

    def __init__(self, title, description, fdp_url):
        self.TITLE = title
        self.DESCRIPTION = description
        self.FDP_URL = fdp_url