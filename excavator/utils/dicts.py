class CascadeDict(dict):
    
    def __init__(self, parents=None, lookup=None, **data):
        self._parents = parents or []
        self._lookup = None
        super().__init__(**data)

    def __missing__(self, key):
        return self._cascade_missing_key(key)

    def __contains__(self, key):
        return (
            super().__contains__(key) or
            self._can_cascade_key(key)
        )

    def _can_cascade_key(self, key):
        for parent in self._parents:
            container = parent
            if self._lookup:
                container = self._lookup(parent)
            if key in container:
                return True
        return False

    def _cascade_missing_key(self, key):
        for parent in self._parents:
            try:
                container = parent
                if self._lookup:
                    container = self._lookup(parent)
                value = parent.__getitem__(key)
                break
            except KeyError as e:
                continue
        else:  # no break
            raise KeyError(key)
        return value

    def __str__(self):
        return '<{}(CascadeDict){}>'.format(
            self.__class__.__name__,
            super().__repr__(),
        )
    __repr__ = __str__


class ComputeDict(dict):

    def __init__(self, **data):
        self._dict = data

    def compute(self, key, value):
        raise NotImplementedError('compute method not implemented')

    def invalidate(self, key):
        super().__delitem__(key)

    def __contains__(self, key):
        return (
            super().__contains__(key) or
            self._can_compute_key(key)
        )

    def __missing__(self, key):
        return self._compute_missing_key(key)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self._dict[key]

    def _can_compute_key(self, key):
        return key in self._dict

    def _compute_missing_key(self, key):
        if key in self._dict:
            self[key] = self.compute(key, self._dict[key])
            return self[key]
        raise KeyError(key)

    def __str__(self):
        return '<{}(ComputeDict){}>'.format(
            self.__class__.__name__,
            super().__repr__(),
        )
    __repr__ = __str__


class ComputeCascadeDict(ComputeDict, CascadeDict):

    def __init__(self, parents=None, lookup=None, **data):
        self._parents = parents or []
        self._lookup = lookup
        self._dict = data

    def __contains__(self, key):
        return (
            # calls ComputeDict.__contains__
            super().__contains__(key) or
            self._can_cascade_key(key)
        )

    def __missing__(self, key):
        try:
            return self._compute_missing_key(key)
        except KeyError:
            return self._cascade_missing_key(key)

    def __str__(self):
        return '<{}(ComputeCascadeDict){}>'.format(
            self.__class__.__name__,
            super().__repr__(),
        )
    __repr__ = __str__
