class CascadeDict(dict):
    
    def __init__(self, parents=None, lookup=None, data=None):
        self._parents = [] if parents is None else parents
        self._lookup = lookup
        super().__init__(**(data or {}))

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
                value = container.__getitem__(key)
                break
            except KeyError as e:
                continue
        else:  # no break
            raise KeyError(key)
        return value

    def cascade_all_keys(self):
        """Returns a set with all possible keys"""
        keys = set(self.keys())
        for parent in self._parents:
            container = parent
            if self._lookup:
                container = self._lookup(parent)
            try:
                keys |= container.cascade_all_keys()
            except AttributeError:
                keys |= set(container.keys())
        return keys

    def cascade_all(self):
        """Returns a dictionary with all possible key-values cascaded"""
        return {key: self[key] for key in self.cascade_all_keys()}

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

    def __setitem__(self, key, value, is_computed=False):
        if not is_computed:
            self._dict[key] = value
        else:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self._dict[key]

    def _can_compute_key(self, key):
        return key in self._dict

    def _compute_missing_key(self, key):
        if key in self._dict:
            self.__setitem__(
                key,
                self.compute(key, self._dict[key]),
                is_computed=True,
            )
            return self[key]
        raise KeyError(key)

    def __str__(self):
        return '<{}(ComputeDict){}>'.format(
            self.__class__.__name__,
            super().__repr__(),
        )
    __repr__ = __str__


class ComputeCascadeDict(ComputeDict, CascadeDict):

    def __init__(self, parents=None, lookup=None, data=None):
        self._parents = parents or []
        self._lookup = lookup
        self._dict = data or {}

    def __contains__(self, key):
        return (
            super().__contains__(key) or  # calls ComputeDict.__contains__
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
