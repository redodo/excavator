from .base import resolve_pattern
from .segments import RawSegment


class TokenSegment(RawSegment):
    def get_value(self):
        if not hasattr(self, '_value') or self._value is None:
            self._value = resolve_pattern(tokens=self.tokens, pattern=self.value)
        return self._value


class LazyTokenSegmentDict(dict):

    def __init__(self, tokens=None):
        self.tokens = tokens or {}

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            if key not in self.tokens:
                raise KeyError("reference to undefined token '%s'" % key)
        value = TokenSegment(self, self.tokens[key])
        self[key] = value
        return value
