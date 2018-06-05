from string import Formatter

from ..regex import re

from .segments import RawSegment, EscapeSegment


class Pattern:
    def __init__(self, tokens, pattern):
        self.tokens = tokens
        self.pattern = pattern
        self.segments = []
        self.build()

    def build(self):
        # check if the pattern should be escaped
        if self.is_regex():
            segment_class = RawSegment
            pattern = self.pattern[1:-1]
        else:
            segment_class = EscapeSegment
            pattern = self.pattern

        # build the segments
        for text, token, _, _ in Formatter().parse(pattern):
            if text:
                self.segments.append(segment_class(self.tokens, text))
            if token:
                self.segments.append(self.tokens[token])

    def is_regex(self):
        return (
            self.pattern.startswith('/') and
            self.pattern.endswith('/') and
            len(self.pattern) > 1
        )

    def get_value(self):
        return ''.join([segment.get_value() for segment in self.segments])

    def compile(self):
        return re.compile(self.get_value())

    def __str__(self):
        return self.get_value()
