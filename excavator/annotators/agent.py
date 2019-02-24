import concurrent.futures

from ..annotations import AnnotationList, AnnotatedText, AnnotatedLine
from .base import Annotator


class Agent:

    def __init__(self):
        self.strategies = list()
        self.corpus = corpus

    def add_strategy(self, strategy, order=None):
        if isinstance(strategy, type):
            strategy = strategy()
        if order is None:
            self.strategies.append(strategy)
        else:
            self.strategies.insert(order, strategy)

    def add_annotator(self, annotator):
        self.annotators.append(annotator)

    def create_annotator(self, *args, **kwargs):
        annotator = Annotator(*args, **kwargs)
        self.annotators.append(annotator)

    def annotate(self, text, strip=True):
        annotated_text = AnnotatedText()

        for line in text.splitlines():
            if strip:
                line = line.strip()
            annotated_line = AnnotatedLine(line)
            annotated_text.lines.append(annotated_line)

            for annotation in self._annotate_all(annotated_line.text):
                annotated_line.annotations.append(annotation)

        for strategy in self.strategies:
            strategy.apply(annotated_text)

        return annotated_text

    def _annotate_all(self, text):
        for annotator in self.annotators:
            yield from annotator.annotate(text)
