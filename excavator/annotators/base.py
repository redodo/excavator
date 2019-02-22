import warnings

from ..annotations import Annotation, Span
from ..patterns import PatternBuilder
from ..regex import re
from ..utils import kwargs_notation, CascadeDict


def transform_patterns(patterns):
    """TODO: move this somewhere else?

    Transforms patterns into a pattern+representation dict
    """

    if isinstance(patterns, str):
        return {(patterns,): None}

    if isinstance(patterns, (list, tuple)):
        return {tuple(patterns): None}

    if isinstance(patterns, dict):
        new_patterns = {}
        for key, value in patterns.items():
            if isinstance(key, (list, tuple)):
                new_patterns[tuple(key)] = value
            else:
                new_patterns[(key,)] = value
        return new_patterns

    raise ValueError('patterns are formatted incorrectly')


# TODO: Merge this with Agent, because it basically is the same thing.
class Corpus:
    """A library of classifiers, settings and tokens
    to be fed to an annotation agent
    """

    default_settings = {
        'case_sensitive': False,
        'do_word_boundary': True,
        # 'do_word_boundary_start': None,  # defaults to `word_boundary`
        # 'do_word_boundary_end': None,    # defaults to `word_boundary`
        'word_boundary_start': r'(?:^|\b)',
        'word_boundary_end': r'(?:\b|$)',
        'fuzzy_costs': '1i+1d+1s',
        'fuzzy_error_rate': 0,
        'fuzzy_min_errors_allowed': 0,

        # colliding matches will yield only the first match
        # TODO: should this be renamed?
        # 'no_collisions': False,

        # Turns on POSIX matching, returning the longest match
        'posix': False,
    }

    def __init__(self, settings=None, tokens=None, classifiers=None):
        self.settings = CascadeDict(self.default_settings, **(settings or {}))
        self.tokens = None or {}
        self.classifiers = None or []


# TODO: Rename this to 'Classifier'
class Annotator:
    """The annotator class.

    :param name: The name of the annotator.  This value is used to
        associate a type with annotations.
    :param tokens: Named tokens that are substituted in the patterns.
        TODO: allow global tokens to be defined and used
    :param patterns: Regex or plaintext patterns to match and create
        annotations from.
    :param case_sensitive: Whether the annotator cares about case.
    :param annotation_class: The class used to instatiate annotations.
    """

    #: The default class used to instantiate annotations.
    default_annotation_class = Annotation

    def __init__(self, name, tokens=None, patterns=None, settings=None,
                 transform=None, annotation_class=default_annotation_class):

        self.name = name
        self.settings = settings or {}
        self.tokens = tokens or {}

        self.patterns = transform_patterns(patterns)

        self.transform = transform
        self.annotation_class = annotation_class

        self._regex_cache = None
        self.compile_patterns()

    def compile_patterns(self):
        if self._regex_cache is None:
            self._regex_cache = {}
            pattern_builder = self.get_pattern_builder()
            for patterns, _ in self.patterns.items():
                for pattern in patterns:
                    if pattern not in self._regex_cache:
                        # TODO: it would probably be better if the pattern builder owned
                        #       the patterns
                        self._regex_cache[pattern] = pattern_builder.compile(pattern)

    def yield_matches(self, text):
        for patterns, representation in self.patterns.items():
            for pattern in patterns:
                regex = self._regex_cache[pattern]
                for match in regex.finditer(text):
                    yield pattern, representation, match

    def annotate(self, text):
        for pattern, representation, match in self.yield_matches(text):

            # By default, the representation is used as the extra data
            # assigned to the annotation.
            data = representation

            # When a transform callback is given, the named groups will
            # be passed to this method, and the result will be used as
            # the extra annotation data.
            if self.transform is not None:
                try:
                    data = self.transform(**match.groupdict())
                except Exception as e:
                    # emit a warning without stopping program execution
                    warnings.warn((
                        'The transform method of annotator {} raised '
                        'an exception when given {} as input:\n'
                        '    {}: {}'
                    ).format(
                        repr(self.get_name()),
                        kwargs_notation(match.groupdict()),
                        e.__class__.__name__,
                        e,
                    ))

            yield self.create_annotation(
                text=match.group(0),
                span=match.span(),
                data=data,
            )

    def get_name(self):
        return self.name

    def get_annotation_class(self):
        return self.annotation_class

    def create_annotation(self, **kwargs):
        kwargs.update(type=self.get_name())
        annotation_class = self.get_annotation_class()
        return annotation_class(**kwargs)

    def get_patterns(self):
        return self.patterns

    def get_pattern_builder(self):
        return PatternBuilder(
            settings=self.settings,
            tokens=self.tokens,
        )
