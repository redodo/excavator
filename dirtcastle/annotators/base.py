import re

from ..annotations.base import Annotation
from ..utils import find_all
from .registry import registry




class AnnotatorBase(type):

    def __new__(cls, name, bases, attrs, **kwargs):
        class Meta:
            """The default meta-class for annotators"""

        meta = attrs.pop('Meta', Meta)

        # determine the type name
        default_type = name.replace('Annotator', '')
        meta.type = getattr(meta, 'type', default_type)

        # create the class
        attrs['_meta'] = meta
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        # add the annotator to the registry when it is not abstract
        abstract = getattr(meta, 'abstract', False)
        if not abstract:
            registry.add(new_class)

        return new_class


class Annotator(metaclass=AnnotatorBase):

    patterns = ()

    case_sensitive = False

    annotation_class = Annotation

    def annotate(self, text):
        """
        Annotates the given text.

        :param text: the string to annotate
            .. note:: This is not an instance of :class:`AnnotatedText`
        :param return: a generator with :class:`Annotation` objects
        """
        raise NotImplementedError(
            '%s does not implement an `annotate` method'
            % self.__class__.__name
        )

    def get_type(self):
        return self._meta.type

    def get_annotation_class(self):
        return self.annotation_class

    def create_annotation(self, **kwargs):
        kwargs.update(type=self.get_type())
        annotation_class = self.get_annotation_class()
        return annotation_class(**kwargs)

    def get_patterns(self):
        return self.patterns

    def get_representation(self, pattern, match):
        patterns = self.get_patterns()
        try:
            return patterns[pattern]
        except (KeyError, TypeError):
            return None

    def is_case_sensitive(self):
        return self.case_sensitive

    class Meta:
        abstract = True


class RegexAnnotator(Annotator):

    def get_flags(self):
        flags = 0
        if not self.is_case_sensitive():
            flags |= re.IGNORECASE
        return flags

    def recompile_patterns(self):
        del self._compiled_patterns
        _ = self.compiled_patterns

    @property
    def compiled_patterns(self):
        if not hasattr(self, '_compiled_patterns'):
            self._compiled_patterns = {}
            flags = self.get_flags()
            for pattern in self.get_patterns():
                regex = re.compile(pattern, flags=flags)
                # regex leads to pattern, pattern leads to representation
                self._compiled_patterns[regex] = pattern
                yield (regex, pattern)
        else:
            yield from self._compiled_patterns.items()

    def annotate(self, text):
        for regex, pattern in self.compiled_patterns:
            for match in regex.finditer(text):
                data = self.get_representation(pattern, match)
                yield self.create_annotation(
                    text=match.group(0),
                    span=match.span(),
                    data=data,
                )

    class Meta:
        abstract = True


class TextAnnotator(Annotator):

    def annotate(self, text):
        case_sensitive = self.is_case_sensitive()
        for pattern in self.get_patterns():
            for found, span in find_all(pattern, text, case_sensitive):
                data = self.get_representation(found, pattern)
                yield self.create_annotation(text=found, span=span, data=data)

    class Meta:
        abstract = True
