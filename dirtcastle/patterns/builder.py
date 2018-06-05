from .base import Pattern
from .tokens import LazyTokenSegmentDict


class RegexBuilder:

    def __init__(self, tokens, patterns):
        self.tokens = LazyTokenSegmentDict(tokens)
        self.patterns = patterns

    def compile_all(self):
        compiled = []
        for pattern in self.patterns:
            compiled.append(Pattern(self.tokens, pattern).compile())
        return compiled
