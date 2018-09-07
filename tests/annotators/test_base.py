from unearth.annotations.base import Annotation
from unearth.annotators.base import Annotator


def test_text_case_sensitivity():
    text = 'hello Hello HELLO'

    annotator = Annotator(
        'Hello',
        patterns=('hello',),
    )
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('hello', (0, 5), type='Hello'),
        Annotation('Hello', (6, 11), type='Hello'),
        Annotation('HELLO', (12, 17), type='Hello'),
    ]

    annotator = Annotator(
        'AlternativeHello',
        patterns=('Hello',),
        settings={'case_sensitive': True},
    )
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('Hello', (6, 11), type='AlternativeHello'),
    ]


def test_representation():
    text = 'hello world'

    annotator = Annotator(
        'HelloWorld',
        patterns={
            'hello': 'Hello',
            'world': 'World',
        },
    )
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('hello', (0, 5), type='HelloWorld', data='Hello'),
        Annotation('world', (6, 11), type='HelloWorld', data='World'),
    ]


def test_regex_case_sensitivity():
    text = 'HELLO Bello cello'

    annotator = Annotator(
        'Thing',
        patterns='/[hbc]ello/',
    )
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('HELLO', (0, 5), type='Thing'),
        Annotation('Bello', (6, 11), type='Thing'),
        Annotation('cello', (12, 17), type='Thing'),
    ]


def test_tokens():
    text = 'hello, world!'

    annotator = Annotator(
        'Thing',
        tokens={
            'comma': ',',
            'dot': '.',
            'sep': '/({comma}|{dot})? /',
        },
        patterns='hello{sep}world!',
    )
    annotations = list(annotator.annotate(text))

    assert annotations == [
        Annotation('hello, world!', (0, 13), type='Thing'),
    ]


def test_complex_tokens():
    text = '''
    40ft
    40'ft
    40"ft
    20ft
    20 feet
    20'feet
    '''

    annotator = Annotator(
        'Container',
        tokens={
            '"': '"',
            "'": "'",
            'feet_symbol': '/({"}|{\'})/',
            'feet_text': '/f(ee)?t/',
            'sep': '/ ?/',
            'feet': '/{sep}{feet_symbol}?{sep}{feet_text}/',
        },
        patterns=(
            '40{feet}',
            '20{feet}',
        ),
    )
    annotations = list(annotator.annotate(text))

    assert len(annotations) == 6


def test_fuzziness():
    text = '''
    h3llo w0rld h311o w0r1d
    H3LLO W0RLD
    '''

    annotator = Annotator(
        'HelloWorld',
        patterns=('hello', 'world'),
        settings={
            'fuzzy_error_rate': 0.1,
            'fuzzy_min_errors_allowed': 1,
        },
    )

    annotations = list(annotator.annotate(text))
    assert len(annotations) == 4


def test_word_boundary():
    text = '1XHello and 2x World Nothing3x'

    annotator = Annotator(
        'Multiply',
        patterns=r'/(?P<amount>\d+)x/',
        transform=lambda amount: int(amount),
        settings={
            'word_boundary_end': False,
        },
    )

    annotations = list(annotator.annotate(text))
    assert len(annotations) == 2
