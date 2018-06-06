from ..annotations import Annotation
from ..patterns import PatternBuilder
from ..regex import re

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

    tokens = {}
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

    def get_tokens(self):
        return self.tokens

    def get_patterns(self):
        return self.patterns

    def get_pattern_builder(self):
        return PatternBuilder(tokens=self.get_tokens())

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

    def prepare_pattern(self, pattern):
        return pattern

    @property
    def compiled_patterns(self):
        if not hasattr(self, '_compiled_patterns'):
            pattern_builder = self.get_pattern_builder()
            self._compiled_patterns = {}
            flags = self.get_flags()
            for raw_pattern in self.get_patterns():
                pattern = pattern_builder.build(raw_pattern)
                prepared_pattern = self.prepare_pattern(pattern.regex)
                regex = re.compile(prepared_pattern, flags=flags)
                # regex leads to pattern, pattern leads to representation
                self._compiled_patterns[regex] = raw_pattern
                yield (regex, raw_pattern)
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


class TextAnnotator(RegexAnnotator):

    def prepare_pattern(self, pattern):
        return r'\b%s\b' % re.escape(pattern)

    class Meta:
        abstract = True
