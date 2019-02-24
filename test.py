from excavator.utils.dicts import CascadeDict


class ReverseSet(set):

    def __init__(self, owner, reverse_attr, *elements):
        self.owner = owner
        self.reverse_attr = reverse_attr
        super().__init__(*elements)

    def add(self, elem, reverse=True):
        super().add(elem)
        if reverse:
            reverse_set = getattr(elem, self.reverse_attr)
            reverse_set.add(self.owner, reverse=False)

    def remove(self, elem, reverse=True):
        super().remove(elem)
        if reverse:
            reverse_set = getattr(elem, self.reverse_attr)
            reverse_set.remove(self.owner, reverse=False)

    def discard(self, elem, reverse=True):
        super().discard(elem)
        if reverse:
            reverse_set = getattr(elem, self.reverse_attr)
            reverse_set.discard(self.owner, reverse=False)

    def clear(self):
        try:
            while True:
                elem = self.pop()
                reverse_set = getattr(elem, self.reverse_attr)
                reverse_set.discard(self.owner, reverse=False)
        except KeyError:
            pass

    # TODO: implement `update`, `intersection_update`, `difference_update`,
    #       and `symmetric_difference_update`


class Node:

    def __init__(self, settings=None):
        self.parents = ReverseSet(self, 'children')
        self.children = ReverseSet(self, 'parents')

        self.settings = CascadeDict(
            self.parents,
            lookup=lambda parent: parent.settings,
            data=(settings or {}),
        )


class Root(Node):
    
    default_settings = {
        'case_sensitive': False,
        'do_word_boundary': True,
        # 'do_word_boundary_start': None,  # defaults to `word_boundary`
        # 'do_word_boundary_end': None,    # defaults to `word_boundary`
        'word_boundary_start': r'(?:^|\b)',
        'word_boundary_end': r'(?:\b|$)',
        'fuzzy_costs': '1i+1d+1s',
        'fuzzy_error_rate': 0,
        'fuzzy_min_errors_allowed': 0,

        # colliding matches will yield only the first match
        # TODO: should this be renamed?
        # 'no_collisions': False,

        # Turns on POSIX matching, returning the longest match
        'posix': False,
    }

    def __init__(self, settings=None):
        self.children = ReverseSet(self, 'parents')

        self.settings = CascadeDict(
            (self.default_settings,),
            data=(settings or {}),
        )


def test_node_integrity():
    A = Node()
    B = Node()

    A.parents.add(B)
    assert A in B.children

    B.children.remove(A)
    assert B not in A.parents

    B.parents.add(A)
    assert B in A.children

    A.children.remove(B)
    assert A not in B.parents

    A.children.add(B)
    A.children.clear()
    assert A not in B.parents

    A.parents.add(B)
    A.parents.clear()
    assert A not in B.children


def test_root_settings():
    root = Root()
    child = Node(settings={'posix': True})
    child.parents.add(root)

    assert child.settings['posix'] == True
    assert child.settings['case_sensitive'] == False
    assert child in root.children

    print(child.settings.cascade_all())


if __name__ == '__main__':
    test_node_integrity()
    test_root_settings()
