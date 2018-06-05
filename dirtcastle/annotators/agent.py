from ..annotations import AnnotationList, AnnotatedText, AnnotatedLine
from .registry import registry


class Agent:

    annotator_classes = registry

    def __init__(self):
        self._strategies = list()

    def get_annotators(self):
        for annotator_class in self.annotator_classes:
            yield annotator_class()

    def add_strategy(self, strategy, order=None):
        if isinstance(strategy, type):
            strategy = strategy()
        if order is None:
            self._strategies.append(strategy)
        else:
            self._strategies.insert(order, strategy)

    def annotate(self, text, strip=True):
        annotated_text = AnnotatedText()

        for line in text.splitlines():
            if strip:
                line = line.strip()
            annotated_line = AnnotatedLine(line)
            annotated_text.lines.append(annotated_line)

            for annotation in self._annotate_all(annotated_line.text):
                annotated_line.annotations.append(annotation)

        for strategy in self._strategies:
            strategy.apply(annotated_text)

        return annotated_text

    def _annotate_all(self, text):
        for annotator in self.get_annotators():
            yield from annotator.annotate(text)


default_agent = Agent()
