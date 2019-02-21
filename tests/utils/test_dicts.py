import pytest

from unearth.utils.dicts import (
    CascadeDict,
    ComputeDict,
    ComputeCascadeDict,
)


def test_cascade_dict():
    a = dict(hello='a', world=True)
    b = CascadeDict(a, hello='b', entry='test')
    c = CascadeDict(b, hello='c', world=False)

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
    b = CascadeDict(a, parent='value', parents='value2', data='value3')

    assert b['hello'] == 'world'
    assert b['parent'] == 'value'
    assert b['parents'] == 'value2'
    assert b['data'] == 'value3'


def test_multiple_parents():
    a1 = dict(hello='world')
    a2 = dict(world='hello')

    b = CascadeDict(a1, a2, something='value')

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
            self.runcount = 0

        def compute(self, key, value):
            self.runcount += 1
            return len(value)

    d = LengthDict(hello='world', len4='test', len6='test12')

    assert 'len4' in d
    assert 'len6' in d

    assert d['hello'] == 5
    assert d['len4'] == 4
    assert d['len6'] == 6

    # invalidation is possible with `del`
    # TODO: or should del remove the value?
    del d['hello']
    assert d['hello'] == 5


def test_compute_cascade_dict():

    class LengthDict(ComputeCascadeDict):
        def compute(self, key, value):
            return len(value)

    a1 = LengthDict(len2='__')
    a2 = LengthDict(len3='___')
    b = LengthDict(a1, a2)
    c = LengthDict(b, len4='____')

    assert 'len2' in a1
    print('\n-- you better assert correctly!')
    assert 'len2' in c
    print('-- did you?')
    assert 'len4' in c

    assert c['len2'] == 2
    assert c['len3'] == 3
    assert c['len4'] == 4
