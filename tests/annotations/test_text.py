import pytest

from dirtcastle.annotations.base import Annotation
from dirtcastle.annotations.list import AnnotationList
from dirtcastle.annotations.text import AnnotatedLine, AnnotatedText


@pytest.fixture
def A():
    return Annotation('hello', (0, 5))


@pytest.fixture
def B():
    return Annotation('world', (0, 5))


@pytest.fixture
def L1(A):
    return AnnotationList([A])


@pytest.fixture
def L2(B):
    return AnnotationList([B])


@pytest.fixture
def T1(L1):
    return AnnotatedLine('hello', L1)


@pytest.fixture
def T2(L2):
    return AnnotatedLine('world', L2)


def test_line_add(A, B, L1, L2, T1, T2):
    T3 = T1 + T2

    # verify integrity of source objects
    assert A.span == (0, 5)
    assert B.span == (0, 5)
    assert T1.annotations == L1 == [A]
    assert T2.annotations == L2 == [B]
    assert T1.text == 'hello'
    assert T2.text == 'world'

    # verify validity of created object
    B2 = Annotation('world', (6, 11))
    assert T3.text == 'hello world'
    assert T3.annotations == [A, B2]


def test_text_init(T1, T2):
    TT = AnnotatedText([T1, T2])
    assert TT.text == 'hello\nworld'
