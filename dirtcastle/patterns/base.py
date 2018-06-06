from string import Formatter

from ..regex import re

from .segments import RawSegment, EscapeSegment


REGEX_PADDING = '/'
REGEX_PADDING_LEN = len(REGEX_PADDING)


def is_regex(s):
    return (
        s.startswith(REGEX_PADDING) and
        s.endswith(REGEX_PADDING) and
        len(s) >= REGEX_PADDING_LEN * 2
    )


def unpad_regex(r):
    return r[REGEX_PADDING_LEN:-REGEX_PADDING_LEN]


class Pattern:

    def __init__(self, tokens, pattern):
        self.tokens = tokens
        self.pattern = pattern

        # Build the regular expression
        segments = []

        # check if the pattern should be escaped
        segment_class = EscapeSegment
        if is_regex(pattern):
            segment_class = RawSegment
            pattern = unpad_regex(pattern)

        # build the segments
        for text, token, _, _ in Formatter().parse(pattern):
            if text:
                segments.append(segment_class(self.tokens, text))
            if token:
                segments.append(self.tokens[token])

        self.regex = ''.join([s.get_value() for s in segments])

    def compile(self, **options):
        return re.compile(self.regex, **options)

    def __repr__(self):
        return '<Pattern(%s -> %s)>' % (
            repr(self.pattern),
            repr(self.regex),
        )

    def __str__(self):
        return self.__repr__()
