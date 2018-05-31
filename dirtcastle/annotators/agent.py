from ..annotations.list import AnnotationList
from ..annotations.text import AnnotatedText, AnnotatedLine
from .registry import registry
from .utils import find_all


class Agent:

    annotator_classes = registry

    def get_annotators(self):
        for annotator_class in self.annotator_classes:
            yield annotator_class()

    def annotate(self, text, strip=True):
        annotated_text = AnnotatedText()

        for line in text.splitlines():
            if strip:
                line = line.strip()
            annotated_line = AnnotatedLine(line)
            annotated_text.lines.append(annotated_line)

            for annotation in self._annotate_all(annotated_line.text):
                annotated_line.annotations.append(annotation)

        return annotated_text

    def _annotate_all(self, text):
        for annotator in self.get_annotators():
            yield from annotator.annotate(text)


default_agent = Agent()
