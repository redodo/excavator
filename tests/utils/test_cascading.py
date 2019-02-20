import pytest

from unearth.utils import CascadingDict


def test_cascading_dict():
    a = dict(hello='a', world=True)
    b = CascadingDict(a, hello='b')
    c = CascadingDict(b, hello='c', world=False)

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
    b = CascadingDict(a, parent='value', parents='value2', data='value3')

    assert b['hello'] == 'world'
    assert b['parent'] == 'value'
    assert b['parents'] == 'value2'
    assert b['data'] == 'value3'


def test_multiple_parents():
    a1 = dict(hello='world')
    a2 = dict(world='hello')

    b = CascadingDict(a1, a2, something='value')

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
