import pytest

from excavator.utils.dicts import (
    CascadeDict,
    ComputeDict,
    ComputeCascadeDict,
)


def test_cascade_dict():
    a = dict(hello='a', world=True)
    b = CascadeDict([a], data=dict(hello='b', entry='test'))
    c = CascadeDict([b], data=dict(hello='c', world=False))

    assert 'hello' in c
    assert 'world' in c
    assert 'world' in b
    assert 'entry' in b

    assert a['hello'] == 'a'
    assert a['world'] == True
    assert b['hello'] == 'b'
    assert b['world'] == True   # this value should be cascaded
    assert c['hello'] == 'c'
    assert c['world'] == False  # this one shouldn't

    a['world'] = False

    assert a['world'] == False
    assert b['world'] == False
    assert c['world'] == False


def test_init_parent():
    a = dict(hello='world')
    b = CascadeDict([a], data=dict(parent='value', parents='value2', data='value3'))

    assert b['hello'] == 'world'
    assert b['parent'] == 'value'
    assert b['parents'] == 'value2'
    assert b['data'] == 'value3'


def test_multiple_parents():
    a1 = dict(hello='world')
    a2 = dict(world='hello')

    b = CascadeDict([a1, a2], data=dict(something='value'))

    assert b['hello'] == 'world'
    assert b['world'] == 'hello'
    assert b['something'] == 'value'

    a1['hello'] = 'hello'
    a2['world'] = 'world'

    assert b['hello'] == 'hello'
    assert b['world'] == 'world'

    del a2['world']
    with pytest.raises(KeyError):
        b['world']

    with pytest.raises(KeyError):
        b['this_does_not_exist']


def test_compute_dict():

    class LengthDict(ComputeDict):

        def __init__(self, **data):
            super().__init__(**data)
            # keep a count to test if the compute function is cached
            self.compute_count = 0

        def compute(self, key, value):
            self.compute_count += 1
            return len(value)

    a = LengthDict(len1='1', len2='12', len3='123', len4='1234', len5='12345')
    assert a['len1'] == 1
    assert a['len1'] == 1
    assert a.compute_count == 1

    # test invalidation
    a.invalidate('len1')
    assert a['len1'] == 1
    assert a.compute_count == 2

    # test deletion
    del a['len1']
    with pytest.raises(KeyError):
        a['len1']

    # test the rest of the keys for correct computation
    assert a['len2'] == 2
    assert a['len3'] == 3
    assert a['len4'] == 4
    assert a['len5'] == 5

    # test if assignment works
    a['len7'] = '1234567'
    assert a['len7'] == 7


def test_compute_cascade_dict():

    class LengthDict(ComputeCascadeDict):
        def compute(self, key, value):
            return len(value)

    a1 = LengthDict(data=dict(len2='__'))
    a2 = LengthDict(data=dict(len3='___'))
    b = LengthDict([a1, a2])
    c = LengthDict([b], data=dict(len4='____'))

    assert 'len2' in a1
    assert 'len2' in c
    assert 'len4' in c

    assert c['len2'] == 2
    assert c['len3'] == 3
    assert c['len4'] == 4
