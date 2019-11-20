class CustomList:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", None)
        self.settings = kwargs.get("settings", None)
        self.found = kwargs.get("found", None)
        self.description = kwargs.get("description", None)
