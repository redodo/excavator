from .base import Pattern
from .tokens import LazyTokenSegmentDict


class PatternBuilder:

    def __init__(self, tokens):
        self.tokens = LazyTokenSegmentDict(tokens)

    def build(self, s):
        return Pattern(self.tokens, s)

    def compile(self, s, **options):
        pattern = Pattern(self.tokens, s)
        return pattern.compile(**options)
