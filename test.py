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
        )


if __name__ == '__main__':
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

    A.parents.add(A)

    print(A.children)
    print(B)
