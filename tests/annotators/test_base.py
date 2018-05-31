from dirtcastle.annotations.base import Annotation
from dirtcastle.annotators.base import TextAnnotator, RegexAnnotator


def test_text_case_sensitivity():
    text = 'hello Hello HELLO'

    class HelloAnnotator(TextAnnotator):
        patterns = ('hello',)

    annotator = HelloAnnotator()
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('hello', (0, 5), type='Hello'),
        Annotation('Hello', (6, 11), type='Hello'),
        Annotation('HELLO', (12, 17), type='Hello'),
    ]

    class AlternativeHelloAnnotator(TextAnnotator):
        case_sensitive = True
        patterns = ('Hello',)

    annotator = AlternativeHelloAnnotator()
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('Hello', (6, 11), type='AlternativeHello'),
    ]


def test_text_representation():
    text = 'hello world'

    class HelloWorldAnnotator(TextAnnotator):
        patterns = {
            'hello': 'Hello',
            'world': 'World',
        }

    annotator = HelloWorldAnnotator()
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('hello', (0, 5), type='HelloWorld', data='Hello'),
        Annotation('world', (6, 11), type='HelloWorld', data='World'),
    ]


def test_regex_case_sensitivity():
    text = 'HELLO Bello cello'

    class ThingAnnotator(RegexAnnotator):
        patterns = (r'[hbc]ello',)

    annotator = ThingAnnotator()
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('HELLO', (0, 5), type='Thing'),
        Annotation('Bello', (6, 11), type='Thing'),
        Annotation('cello', (12, 17), type='Thing'),
    ]


def test_regex_representation():
    text = 'hello world'

    class HelloWorldAnnotator(RegexAnnotator):
        patterns = {
            'hello': 'Hello',
            'world': 'World',
        }

    annotator = HelloWorldAnnotator()
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('hello', (0, 5), type='HelloWorld', data='Hello'),
        Annotation('world', (6, 11), type='HelloWorld', data='World'),
    ]


def test_regex_recompile():
    text = 'hello world'

    class ThingAnnotator(RegexAnnotator):
        patterns = ('hello',)

    annotator = ThingAnnotator()
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('hello', (0, 5), type='Thing'),
    ]

    annotator.patterns += ('world',)
    annotator.recompile_patterns()
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('hello', (0, 5), type='Thing'),
        Annotation('world', (6, 11), type='Thing'),
    ]
