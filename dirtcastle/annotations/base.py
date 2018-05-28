from .span import Span


class Annotation:

    def __init__(self, text, span, type=None, score=1.0, data=None):
        self.text = text
        self.span = Span(span)
        self.type = type
        self.score = score

    def copy(self):
        return Annotation(
            text=self.text,
            span=self.span,
            type=self.type,
            score=self.score,
        )

    def __repr__(self):
        return '<Annotation({text}, span={span}, type={type}, score={score})>'.format(
            text=repr(self.text),
            span=repr(self.span),
            type=repr(self.type),
            score=repr(self.score),
        )

    def __eq__(self, other):
        if not isinstance(other, Annotation):
            return NotImplemented

        return (
            self.text == other.text and
            self.span == other.span and
            self.type == other.type and
            self.score == other.score
        )

    def __hash__(self):
        return super().__hash__()
