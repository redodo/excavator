from dirtcastle.annotators import Agent

from .models import Annotator


def create_annotation_agent():
    agent = Agent()

    for annotator in Annotator.objects.all():
        patterns = {}

        # TODO: add support for tokens (global and local)

        # populate documentless patterns
        for pattern in annotator.patterns.values_list('pattern', flat=True):
            patterns[pattern] = None

        # populate patterns with documents
        for document in annotator.documents.all():
            document_patterns = tuple(document.patterns.values_list('pattern', flat=True))
            patterns[document_patterns] = document.data

        agent.create_annotator(annotator.name, patterns=patterns)

    return agent
