from ..regex import re

from .base import resolve_pattern
from .tokens import LazyTokenSegmentDict


class PatternBuilder:

    def __init__(self, settings=None, tokens=None):
        # !! The settings and tokens of the pattern builder never differ from
        # the settings and tokens of the classifier (merge?)
        # TODO: Use corpus settings when they're ready
        self.settings = self.default_settings.copy()
        self.settings.update(settings or {})

        self.tokens = LazyTokenSegmentDict(**(tokens or {}))

    def get_flags(self):
        flags = 0
        if not self.settings['case_sensitive']:
            flags |= re.IGNORECASE
        return flags

    def build(self, s):
        pattern = resolve_pattern(self.tokens, s)

        # TODO: the settings should not be evaluated at every pattern build
        #       Figure out a better place to do this...

        # apply fuzzy config
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

        # apply word boundaries
        do_word_boundary = self.settings['do_word_boundary']
        do_word_boundary_start = self.settings.get(
            'do_word_boundary_start',
            do_word_boundary,
        )
        do_word_boundary_end = self.settings.get(
            'do_word_boundary_end',
            do_word_boundary,
        )
        if do_word_boundary_start:
            pattern = self.settings['word_boundary_start'] + pattern
        if do_word_boundary_end:
            pattern = pattern + self.settings['word_boundary_end']

        if self.settings['posix']:
            pattern = r'(?p)' + pattern

        return pattern

    def compile(self, s):
        return re.compile(self.build(s), flags=self.get_flags())
