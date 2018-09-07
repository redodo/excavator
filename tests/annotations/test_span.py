import json
import pytest

from unearth.annotations.span import Span


def test_init():
    assert Span([1, 2]) == Span(1, 2)
    assert Span(1, 0) == Span(0, 1)
    assert Span(Span(1, 2)) == Span(1, 2)
    assert Span((1, 2)) == Span(1, 2)
    assert Span(slice(1, 3)) == Span(1, 3)


def test_attributes():
    span = Span(1, 2)
    assert span.start == 1
    assert span.end == 2
    assert span.length == 1


def test_validation():
    with pytest.raises(ValueError):
        a = Span(1)
    with pytest.raises(ValueError):
        a = Span('a', 'b')
    with pytest.raises(ValueError):
        a = Span([1])


def test_contains():
    assert Span(1, 3) in Span(2, 5)
    assert Span(4, 4) in Span(1, 5)
    assert 3 in Span(1, 4)
    assert 0 not in Span(1, 3)

    assert [2, 5] in Span(1, 3)
    assert (2, 5) in Span(3, 5)

    assert Span(2, 6) in Span(4, 6)
    assert Span(4, 6) in Span(2, 6)
    assert Span(2, 4) in Span(2, 6)
    assert Span(2, 6) in Span(2, 4)

    assert 5 not in Span(2, 5)
    assert 4 in Span(2, 5)
    assert 2 in Span(2, 5)

    assert Span(4, 4) not in Span(2, 4)

    assert Span(2, 4) in Span(3, 4)
    assert Span(3, 4) in Span(2, 4)

    assert Span(2, 4) not in Span(0, 2)
    assert Span(0, 2) not in Span(2, 4)

    assert Span(11, 13) in Span(11, 13)


def test_lt():
    assert Span(1, 3) < Span(1, 2)
    assert not Span(1, 2) < Span(0, 4)


def test_le():
    assert Span(1, 3) <= Span(1, 3)
    assert Span(1, 4) <= Span(1, 3)


def test_gt():
    assert Span(1, 3) > Span(1, 5)
    assert not Span(0, 4) > Span(3, 3)


def test_ge():
    assert Span(2, 5) >= Span(2, 5)
    assert Span(2, 5) >= Span(2, 7)


def test_eq():
    assert Span(1, 2) == Span(1, 2)
    assert Span(3, 4) == Span(3, 4)
    assert Span(1, 3) != Span(1, 4)


def test_add():
    assert Span(1, 3) + 3 == Span(4, 6)


def test_sub():
    assert Span(0, 2) - 2 == Span(-2, 0)


def test_len():
    assert len(Span(0, 5)) == 5
    assert len(Span(0, 0)) == 0


def test_json():
    span = Span(1, 4)

    json_span = json.dumps(span)
    assert json_span == '[1, 4]'

    rebuilt = Span(json.loads(json_span))
    assert span == rebuilt
