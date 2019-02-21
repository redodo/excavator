from ..utils import ComputeCascadeDict, ComputeDict

from .base import resolve_pattern
from .segments import RawSegment


class TokenSegment(RawSegment):
    def get_value(self):
        if not hasattr(self, '_value') or self._value is None:
            self._value = resolve_pattern(tokens=self.tokens, pattern=self.value)
        return self._value


class LazyTokenSegmentDict(ComputeDict):
    def compute(self, key, value):
        print(f'called compute with "{key}": "{value}"')
        return TokenSegment(self, value)
