class CascadingDict(dict):
    
    def __init__(self, *parents, **data):
        self.__parents = parents
        super().__init__(**data)

    def __missing__(self, key):
        for parent in self.__parents:
            try:
                value = parent.__getitem__(key)
                break
            except KeyError as e:
                continue
        else:  # no break
            raise KeyError(key)
        return value
