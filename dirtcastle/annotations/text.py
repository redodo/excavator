from ..utils import JsonSerializer
from .base import Annotation
from .span import Span
from .list import AnnotationList


class AnnotatedText(JsonSerializer):

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
            line.annotations.disambiguate(*args, **kwargs)

    def __eq__(self, other):
        if not isinstance(other, AnnotatedText):
            return False
        return self.lines == other.lines

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

    def to_dict(self):
        return {
            'lines': self.lines,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            lines=d.get('lines', None),
        )


class AnnotatedLine(JsonSerializer):

    JOIN_CHAR = ' '

    def __init__(self, text='', annotations=None):
        self.text = text

        if isinstance(annotations, AnnotationList):
            self.annotations = annotations
        else:
            self.annotations = AnnotationList(annotations or [])

    @property
    def cells(self):
        return self.annotations.cells

    def copy(self):
        return AnnotatedLine(
            text=self.text,
            annotations=self.annotations.copy(),
        )

    def __eq__(self, other):
        if not isinstance(other, AnnotatedLine):
            return False
        return self.text == other.text and self.annotations == other.annotations

    def __add__(self, other):
        if other == 0:
            # this statement allows AnnotatedLine to work with sum()
            return self

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
    
    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        return '<AnnotatedLine({text}, annotations={annotations})>'.format(
            text=repr(self.text),
            annotations=repr(self.annotations),
        )

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        return {
            'text': self.text,
            'annotations': self.annotations,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            text=d.get('text', None),
            annotations=AnnotationList(d.get('annotations', None)),
        )
