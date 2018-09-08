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


def resolve_pattern(tokens, pattern):
    """TODO: rename this function

    This function extracts fills token values in a pattern and escapes
    plaintext.
    """
    segments = []

    # check if the pattern should be escaped
    segment_class = EscapeSegment
    if is_regex(pattern):
        segment_class = RawSegment
        pattern = unpad_regex(pattern)

    # build the segments
    for text, token, _, _ in Formatter().parse(pattern):
        if text:
            segments.append(segment_class(tokens, text))
        if token and ',' not in token:
            # TODO: fix collisions with the following syntax *better*:
            #           a{,2}b{3,5}c{4}
            segments.append(tokens[token])

    return ''.join([s.get_value() for s in segments])
