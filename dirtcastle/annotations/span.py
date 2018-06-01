# The start and end indices for compatibility with regular lists and tuples
START = 0
END = 1


class Span(tuple):

    LIST_TYPES = (list, tuple)

    def __new__(cls, start, end=None):
        if callable(start):
            start = start()

        if isinstance(start, slice):
            end = start.stop
            start = start.start

        if isinstance(start, cls.LIST_TYPES):
            start, end = start
        elif end is None:
            raise ValueError('span end required')

        try:
            start, end = int(start), int(end)
        except ValueError:
            raise ValueError('start and end must both be integers')

        if end < start:
            start, end = end, start

        return super().__new__(cls, (start, end))

    def __spanesque(self, obj):
        return isinstance(obj, Span) or (
            isinstance(obj, self.LIST_TYPES) and
            len(obj) == 2
        )

    @property
    def start(self):
        return self[START]

    @property
    def end(self):
        return self[END]

    @property
    def length(self):
        return self.__len__()

    def __len__(self):
        return self[END] - self[START]

    def __add__(self, other):
        return Span(
            self[START] + other,
            self[END] + other,
        )

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        return Span(
            self[START] - other,
            self[END] - other,
        )

    def __isub__(self, other):
        return self - other

    def __contains__(self, other):
        if self.__spanesque(other):
            return (
                self[START] <= other[START] < self[END] or
                self[START] < other[END] < self[END]
            ) or (
                other[START] <= self[START] < other[END] or
                other[START] < self[END] < other[END]
            )

        return self[START] <= other < self[END]

    def __lt__(self, other):
        if self.__spanesque(other):
            return self[START] < other[START] or (
                self[START] == other[START] and
                self[END] > other[END]
            )

        return self[END] <= other

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if self.__spanesque(other):
            return self[START] > other[START] or (
                self[START] == other[START] and
                self[END] < other[END]
            )
        return self[START] > other

    def __ge__(self, other):
        return self == other or self > other

    def __bool__(self):
        return None not in self

    def __repr__(self):
        return '<Span({start}, {end})>'.format(
            start=self.start,
            end=self.end,
        )

    def __str__(self):
        return self.__repr__()
