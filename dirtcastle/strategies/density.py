from ..annotations import AnnotatedLine

from .base import Strategy


class IncreaseDensityStrategy(Strategy):

    TEXT = 'text'
    ANNOTATIONS = 'annotations'

    def __init__(self, threshold, metric=TEXT, include_empty=False, tries=3):
        self.threshold = threshold
        self.metric = metric
        self.include_empty = include_empty
        self.tries = tries

    def apply(self, text):
        for _ in range(self.tries):
            try:
                density = self.compute_density(text)
            except ZeroDivisionError:
                # annotated text is empty
                break
            if density < self.threshold:
                self.fold_lines(text)

    def compute_density(self, text):
        densities = []
        for line in text.lines:
            if not self.is_empty(line) or self.include_empty:
                if self.metric == self.TEXT:
                    densities.append(len(line.text.strip()))
                elif self.metric == self.ANNOTATIONS:
                    densities.append(len(line.annotations))
                else:
                    raise ValueError("unsupported metric '%s'" % self.metric)
        return sum(densities) / len(densities)

    def fold_lines(self, text):
        folded_lines = []

        current_lines = []
        for line in text.lines:
            if not self.is_empty(line):
                current_lines.append(line)
            elif not current_lines:
                folded_lines.append(AnnotatedLine())
            else:
                folded_lines.append(sum(current_lines))
                current_lines = []
        
        if current_lines:
            folded_lines.append(sum(current_lines))

        text.lines = folded_lines

    def is_empty(self, line):
        return not line.text.strip()
