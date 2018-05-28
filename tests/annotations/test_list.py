from dirtcastle.annotations.base import Annotation
from dirtcastle.annotations.list import AnnotationList


def test_combinations():
    A1 = Annotation('hello', (0, 4))
    A2 = Annotation('hell', (0, 3))
    A3 = Annotation('hello world', (0, 10))
    B1 = Annotation('world', (6, 10))
    B2 = Annotation('worl', (6, 9))
    B3 = Annotation('world!', (6, 11))
    C = Annotation('!', (11, 11))

    annotations = AnnotationList([A1, A2, A3, B1, B2, B3, C])

    assert set(annotations.combinations()) == {
        (A1, B1, C),
        (A1, B2, C),
        (A1, B3),
        (A2, B1, C),
        (A2, B2, C),
        (A2, B3),
        (A3, C),
    }


def test_ordering():
    A = Annotation('hello', (0, 4))
    B = Annotation('hell', (0, 3))
    C = Annotation('world', (6, 10))

    annotations = AnnotationList([C, A])
    annotations.append(B)

    assert annotations.index(A) == 0
    assert annotations.index(B) == 1
    assert annotations.index(C) == 2


def test_disambiguate():
    A1 = Annotation('hello', (0, 4), score=1.1)
    A2 = Annotation('hell', (0, 3), score=1.0)
    B = Annotation('world', (6, 10), score=1.1)

    annotations = AnnotationList([A1, A2, B])

    assert annotations.disambiguate() == (A1, B)
    assert A2 in annotations

    annotations.disambiguate(discard_others=True)
    assert A2 not in annotations


def test_cells():
    A1 = Annotation('hello', (0, 4), type='Greeting')
    A2 = Annotation('hell', (0, 3), type='Place')
    B1 = Annotation('world!', (6, 11), type='Place')
    B2 = Annotation('world', (6, 10), type='Place')
    C = Annotation('!', (11, 11), type='Symbol')

    annotations = AnnotationList([A1, A2, B1, B2, C])
    assert annotations.cells == [
        [A1, A2],
        [B1, B2],
        [C],
    ]


def test_filter_and_boost():
    A1 = Annotation('hello', (0, 4), type='Greeting', score=1.0)
    A2 = Annotation('hell', (0, 3), type='Place', score=1.0)
    B = Annotation('world', (6, 10), type='Place', score=1.0)

    annotations = AnnotationList([A1, A2, B])

    assert annotations.filter(type='Greeting') == [A1]
    assert annotations.filter(type='Place') == [A2, B]

    annotations.filter(type='Greeting').boost(1.25)
    assert A1.score == 1.25
    assert A2.score == 1.0
    assert B.score == 1.0

    annotations.cells[0].filter(type='Place').boost(1.50)
    assert A1.score == 1.25
    assert A2.score == 1.50
    assert B.score == 1.0

    annotations.cells[1].boost(1.75)
    assert A1.score == 1.25
    assert A2.score == 1.50
    assert B.score == 1.75
