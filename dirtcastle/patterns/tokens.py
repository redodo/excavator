from .base import Pattern
from .segments import PatternSegment


class TokenSegment(PatternSegment):
    def get_value(self):
        if not hasattr(self, '_value') or self._value is None:
            pattern = Pattern(tokens=self.tokens, pattern=self.value)
            self._value = pattern.regex
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
