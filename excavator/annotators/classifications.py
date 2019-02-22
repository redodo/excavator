class Corpus:

    tokens = None
    settings = None

    def __init__(self, tokens):
        pass


class Classification:

    tokens = None    # TODO: make token dict cascading with corpus tokens
    settings = None  # TODO: make settings dict cascading with corpus settings

    def __init__(self, corpus):
        self.corpus = corpus

    def compile_pattern(self, pattern):
        """Compiles the pattern after resolving its tokens"""


class ComputedClassification(Classification):
    """TODO: Should this be renamed?

    This classification has the following data:
        - a list of patterns
        - a transform function

    It matches the patterns against a given text.  Every match is passed
    to the transform function and set in the annotation representation
    field.

    This allows annotation representations to be dynamic, which is
    required for classifications such as Time, Date, Number, etc.
    """


class DocumentClassification(Classification):
    """TODO: Should this be renamed?

    This classification has the following data:
        - a list of documents (or representations, identifiers...)
        - a list of patterns for each document

    All patterns are matched against a given text.  When a match is
    found, the document is set in the annotation representation field.
    """
