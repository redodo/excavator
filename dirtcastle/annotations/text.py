from .base import Annotation
from .span import Span
from .list import AnnotationList


class AnnotatedTest:
    pass


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
            annotations=self.annotations.copy()
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
