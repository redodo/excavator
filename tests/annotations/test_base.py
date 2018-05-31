import json

from dirtcastle.annotations.base import Annotation


def test_eq():
    A = Annotation('hello', (0, 4), type='Greeting', score=1.0)
    B = Annotation('hello', (0, 4), type='Greeting', score=1.0)
    C = Annotation('world', (0, 4), type='Place', score=1.0)

    assert A == B
    assert A is not B
    assert A != C
