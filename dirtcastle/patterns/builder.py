from ..regex import re

from .base import resolve_pattern
from .tokens import LazyTokenSegmentDict


class PatternBuilder:

    def __init__(self, tokens):
        self.tokens = LazyTokenSegmentDict(tokens)

    def build(self, s):
        return resolve_pattern(self.tokens, s)

    def compile(self, s, **options):
        return re.compile(self.build(s), **options)
