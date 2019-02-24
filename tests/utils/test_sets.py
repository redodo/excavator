import pytest

from excavator.utils.sets import ReverseSet


class Node:
    def __init__(self):
        self.parents = ReverseSet(self, 'children')
        self.children = ReverseSet(self, 'parents')


@pytest.fixture
def A():
    return Node()

@pytest.fixture
def B():
    return Node()

@pytest.fixture
def C():
    return Node()


def test_reverse_set_add(A, B):
    A.parents.add(B)
    assert A in B.children
    assert B in A.parents


def test_reverse_set_remove(A, B):
    A.children.add(B)
    A.children.remove(B)
    assert B not in A.children
    assert A not in B.parents


def test_reverse_set_clear(A, B):
    A.children.add(B)
    A.children.clear()
    assert A not in B.parents


def test_reverse_set_update(A, B, C):
    A.children.update([B, C])
    assert B in A.children
    assert C in A.children
    assert A in B.parents
    assert A in C.parents
