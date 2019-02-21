class CascadeDict(dict):
    
    def __init__(self, *parents, **data):
        self._parents = parents
        super().__init__(**data)

    def __missing__(self, key):
        return self._cascade_missing_key(key)

    def __contains__(self, key):
        print('Calling CascadeDict.__contains__')
        return (
            super().__contains__(key) or
            self._key_in_parent(key)
        )

    def _key_in_parent(self, key):
        for parent in self._parents:
            if key in parent:
                return True
        return False

    def _cascade_missing_key(self, key):
        for parent in self._parents:
            try:
                value = parent.__getitem__(key)
                break
            except KeyError as e:
                continue
        else:  # no break
            raise KeyError(key)
        return value


class ComputeDict(dict):

    def __init__(self, **data):
        self._items = data

    def compute(self, key, value):
        raise NotImplementedError('compute method not implemented')

    def __contains__(self, key):
        print('Calling ComputeDict.__contains__')
        return key in self._items

    def __missing__(self, key):
        return self._compute_missing_key(key)

    def _compute_missing_key(self, key):
        if key in self._items:
            self[key] = self.compute(key, self._items[key])
            return self[key]
        print('<-- gonna raise a keyerror here')
        raise KeyError(key)


class ComputeCascadeDict(ComputeDict, CascadeDict):

    def __init__(self, *parents, **data):
        self._parents = parents
        self._items = data

        print('initting dict')
        print(f'_parents = {parents}')
        print(f'_items = {data}')
        super().__init__()

    def __contains__(self, key):
        return (
            key in self._items or
            self._key_in_parent(key)
        )

    def __missing__(self, key):
        try:
            return self._compute_missing_key(key)
        except KeyError:
            print('lets cascade!')
            return self._cascade_missing_key(key)
