from ..regex import re


class RawSegment:

    def __init__(self, tokens, value):
        self.tokens = tokens
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return self.get_value()


class EscapeSegment(RawSegment):
    def get_value(self):
        return re.escape(self.value)
