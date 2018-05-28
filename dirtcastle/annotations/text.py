from .base import Annotation
from .span import Span
from .list import AnnotationList


class AnnotatedText:

    def __init__(self, lines=None):
        self.lines = lines or []

    def copy(self):
        return AnnotatedText(
            lines=[line.copy() for line in self.lines]
        )

    @property
    def text(self):
        return '\n'.join([line.text for line in self.lines])

    def disambiguate(self, *args, **kwargs):
        for line in self.lines:
            line.disambiguate(*args, **kwargs)

    def __repr__(self):
        rep = '<AnnotatedText(lines=[{}])>'

        if len(self.lines) == 0:
            return rep.format('')

        return rep.format((
            '\n    ' +
            ',\n    '.join([repr(line) for line in self.lines]) +
            ',\n'
        ))

    def __str__(self):
        return self.__repr__()


class AnnotatedLine:

    JOIN_CHAR = ' '

    def __init__(self, text, annotations=None):
        self.text = text

        if isinstance(annotations, AnnotationList):
            self.annotations = annotations
        else:
            self.annotations = AnnotationList(annotations or [])

    def copy(self):
        return AnnotatedLine(
            text=self.text,
            annotations=self.annotations.copy(),
        )

    def __add__(self, other):
        if not isinstance(other, AnnotatedLine):
            return NotImplemented

        copy = self.copy()
        copy.text += self.JOIN_CHAR
        offset = len(copy.text)

        for other_annotation in other.annotations:
            annotation = other_annotation.copy()
            annotation.span += offset
            copy.annotations.append(annotation)

        copy.text += other.text
        return copy

    def __repr__(self):
        return '<AnnotatedLine({text}, annotations={annotations})>'.format(
            text=repr(self.text),
            annotations=repr(self.annotations),
        )

    def __str__(self):
        return self.__repr__()
