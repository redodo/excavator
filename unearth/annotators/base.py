import warnings

from ..annotations import Annotation, Span
from ..patterns import PatternBuilder
from ..regex import re
from ..utils import kwargs_notation


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

    #: The default settings
    default_settings = {
        'case_sensitive': False,
        'word_boundary': True,
        'word_boundary_start': None,  # defaults to `word_boundary`
        'word_boundary_end': None,    # defaults to `word_boundary`
        'fuzzy_costs': '1i+1d+1s',
        'fuzzy_error_rate': 0,
        'fuzzy_min_errors_allowed': 0,

        # colliding matches will yield only the first match
        # TODO: should this be renamed?
        'no_collisions': False,
    }

    WORD_BOUNDARY_START = r'(?:^|\b)'
    WORD_BOUNDARY_END = r'(?:\b|$)'

    def __init__(self, name, tokens=None, patterns=None, settings=None,
                 transform=None, annotation_class=default_annotation_class):

        self.name = name
        self.tokens = tokens or {}

        self.patterns = transform_patterns(patterns)

        self.settings = self.default_settings.copy()
        self.settings.update(settings or {})

        self.transform = transform
        self.annotation_class = annotation_class

        self._regex_cache = None
        self.precache_patterns()

    def precache_patterns(self):
        if self._regex_cache is None:
            self._regex_cache = {}
            pattern_builder = self.get_pattern_builder()
            for patterns, _ in self.patterns.items():
                for pattern in patterns:
                    if pattern not in self._regex_cache:
                        built_pattern = pattern_builder.build(pattern)
                        built_pattern = self.prepare_pattern(built_pattern)

                        regex = re.compile(built_pattern, flags=self.get_flags())
                        self._regex_cache[pattern] = regex

    def yield_matches(self, text):
        for patterns, representation in self.patterns.items():
            for pattern in patterns:
                regex = self._regex_cache[pattern]
                for match in regex.finditer(text):
                    yield pattern, representation, match

    def annotate(self, text):
        if self.settings['no_collisions']:
            reserved_spans = []

        for pattern, representation, match in self.yield_matches(text):

            if self.settings['no_collisions']:
                ignore_match = False
                span = Span(match.span())
                for reserved_span in reserved_spans:
                    if span in reserved_span:
                        ignore_match = True
                        break
                if ignore_match:
                    continue
                reserved_spans.append(span)

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

    def prepare_pattern(self, pattern):
        # TODO: Implement pattern pre-processors for word_boundary and
        #       fuzziness. Post-processors as well? (for time representation)

        allowed_errors = max(
            self.settings['fuzzy_min_errors_allowed'],
            int(len(pattern) * self.settings['fuzzy_error_rate']),
        )
        if allowed_errors > 0:
            pattern = r'(?e)(?:%s){%s<=%i}' % (
                pattern,
                self.settings['fuzzy_costs'],
                allowed_errors,
            )

        word_boundary_start = self.settings['word_boundary_start']
        if word_boundary_start is None:
            word_boundary_start = self.settings['word_boundary']

        word_boundary_end = self.settings['word_boundary_end']
        if word_boundary_end is None:
            word_boundary_end = self.settings['word_boundary']

        if word_boundary_start:
            pattern = self.WORD_BOUNDARY_START + pattern
        if word_boundary_end:
            pattern = pattern + self.WORD_BOUNDARY_END

        return pattern

    def get_name(self):
        return self.name

    def get_flags(self):
        flags = 0
        if not self.settings['case_sensitive']:
            flags |= re.IGNORECASE
        return flags

    def get_annotation_class(self):
        return self.annotation_class

    def create_annotation(self, **kwargs):
        kwargs.update(type=self.get_name())
        annotation_class = self.get_annotation_class()
        return annotation_class(**kwargs)

    def get_tokens(self):
        return self.tokens

    def get_patterns(self):
        return self.patterns

    def get_pattern_builder(self):
        return PatternBuilder(tokens=self.get_tokens())
