from ..regex import re


class PatternSegment:

    def __init__(self, tokens, value):
        self.tokens = tokens
        self.value = value

    def get_value(self):
        raise NotImplementedError(
            '%s does not implement the `get_value` method'
            % self.__class__.__name
        )

    def __str__(self):
        return self.get_value()


class EscapeSegment(PatternSegment):
    def get_value(self):
        return re.escape(self.value)


class RawSegment(PatternSegment):
    def get_value(self):
        return self.value
