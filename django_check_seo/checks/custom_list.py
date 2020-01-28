class CustomList:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", None)
        self.settings = kwargs.get("settings", None)
        self.found = kwargs.get("found", None)
        self.searched_in = kwargs.get("searched_in", [])
        self.description = kwargs.get("description", None)
